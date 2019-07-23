from apas.util.logging import LogHandler

import xml.etree.ElementTree as ET
from typing import Callable
from copy import deepcopy

import time
import re


class BrowseNodeCrawler:
    HEADER = "{0: <20}".format("(NodeCrawler):")

    MAIN_CATEGORIES = {
        "books": [
            "Biografien & Erinnerungen",
            "Börse & Geld",
            "Business & Karriere",
            "Comics & Mangas",
            "Computer & Internet",
            "Erotik",
            "Esoterik",
            "Fachbücher",
            "Fantasy & Science Fiction",
            "Film, Kunst & Kultur",
            "Freizeit, Haus & Garten",
            "Geschenkbücher",
            "Jugendbücher",
            "Kalender",
            "Kinderbücher",
            "Kochen & Genießen",
            "Krimis & Thriller",
            "Liebesromane",
            "Literatur & Fiktion",
            "Medizin",
            "Naturwissenschaften & Technik",
            "Politik & Geschichte",
            "Ratgeber",
            "Recht",
            "Reise & Abenteuer",
            "Religion & Glaube",
            "Schule & Lernen",
            "Sozialwissenschaft",
            "Sport & Fitness",
        ],
        "kindle_books": [
            'Belletristik',
            'Biografien & Erinnerungen',
            'Business & Karriere',
            'Börse & Geld',
            'Comics & Mangas',
            'Computer & Internet',
            'Erotik',
            'Esoterik',
            'Fachbücher',
            'Fantasy & Science Fiction',
            'Freizeit, Haus & Garten',
            'Jugendbücher',
            'Kinderbücher',
            'Kochen & Genießen',
            'Krimis & Thriller',
            'Lernen & Nachschlagen',
            'Liebesromane', 'Musiknoten',
            'Naturwissenschaften & Technik',
            'Politik & Geschichte',
            'Ratgeber',
            'Reise & Abenteuer',
            'Religion & Glaube',
            'Sport & Fitness',
            'Fremdsprachige eBooks'
        ]
    }

    FIELD_NAMES_TOP_BOOKS_old = [
        "category",
        "category-1",
        "category-2",
        "category-3",
        "asin",
        "title",
        "sales_rank",
        "offer_url",
    ]

    FIELD_NAMES_TOP_BOOKS = ["asin", "title", "sales_rank", "offer_url"]

    FILE_NAME_SUFFIX_TOP_BOOKS = "_top_books.csv"

    FIELD_NAMES_CATEGORIES = ["parent_category", "category"]

    FILE_NAME_SUFFIX_CATEGORIES_TREE = "discovered_categories.json"

    NODE_ID_TO_PRODUCT_TYPE = {
        '541686': "books",
        '530485031': "kindle_books",
        '530886031': "kindle_books",
        # '530887031': "kindle_newsstand"  Not yet implemented
    }

    def __init__(
        self, api_handler, file_handler, config_dict: dict,
            verbose: bool = False) -> None:
        self.verbose = verbose

        self.check_config(config_dict=config_dict)
        self.config_dict = config_dict

        self.INCLUDED_MAIN_CATEGORIES = {
            "books": self.config_dict["BrowseNodeCrawler"]['books']["INCLUDED_MAIN_CATEGORIES"],
            "kindle_books": self.config_dict["BrowseNodeCrawler"]['kindle_books']["INCLUDED_MAIN_CATEGORIES"],
        }
        self.SPECIFIC_SUB_CATEGORIES = {
            "books": self.config_dict["BrowseNodeCrawler"]['books']["SPECIFIC_SUB_CATEGORIES"],
            "kindle_books": self.config_dict["BrowseNodeCrawler"]['kindle_books']["SPECIFIC_SUB_CATEGORIES"]
        }

        self.PRODUCT_LIMIT = int(self.config_dict["PRODUCT_LIMIT"])

        self.api_handler = api_handler
        self.file_handler = file_handler

        self.category_tree = {}
        self.categories_paths = []

        self.product_type = ""

    @classmethod
    def check_config(cls, config_dict: dict):
        necessary_variables = {
            "BrowseNodeCrawler": {
                "books": [
                    "INCLUDED_MAIN_CATEGORIES",
                    "SPECIFIC_SUB_CATEGORIES",
                ],
                "kindle_books": [
                    "INCLUDED_MAIN_CATEGORIES",
                    "SPECIFIC_SUB_CATEGORIES",
                ],
            }
        }

        error_msg = (
            f"{cls.HEADER} Invalid config-File. The following variable is missing: %s"
        )

        for module, variables_list in necessary_variables.items():
            if module not in config_dict.keys():
                raise Exception(error_msg.replace("%s", module))
            else:
                for variable_name in variables_list:
                    if variable_name not in config_dict[module].keys():
                        raise Exception(error_msg.replace("%s", variable_name))

    def run_crawler(self, browse_node_id: int = '541686'):
        self.product_type = self.NODE_ID_TO_PRODUCT_TYPE[str(browse_node_id).lower()]

        final_rank_rows = []
        categories_list = [self.product_type.capitalize()]

        if self.SPECIFIC_SUB_CATEGORIES[self.product_type]:
            category_discovery = False
            for sub_category in self.SPECIFIC_SUB_CATEGORIES[self.product_type]:
                node_id = sub_category.split('[')[1][:-1]

                browse_nodes = self.api_handler.api_call_with_retry(
                    function=self.api_handler.browse_node_lookup,
                    function_params={"BrowseNodeId": node_id},
                )

                if not browse_nodes:
                    print("ERROR")
                    return False

                final_rank_rows = self.walk_through_categories(
                    recursive_func=self.walk_through_categories,
                    browse_nodes=browse_nodes,
                    final_rank_rows=final_rank_rows,
                    categories_list=categories_list,
                    current_level=0,
                )

        else:
            category_discovery = True
            browse_nodes = self.api_handler.api_call_with_retry(
                function=self.api_handler.browse_node_lookup,
                function_params={"BrowseNodeId": browse_node_id},
            )

            final_rank_rows = self.walk_through_categories(
                recursive_func=self.walk_through_categories,
                browse_nodes=browse_nodes,
                final_rank_rows=final_rank_rows,
                categories_list=categories_list,
                current_level=0,
            )

        try:
            deepest_sub_category_level = max(
                [len(l["category"]) for l in final_rank_rows]
            )

            categories_field_names = []
            for level in range(0, deepest_sub_category_level):
                categories_field_names.append(f"category-{level}")

            self.FIELD_NAMES_TOP_BOOKS = (
                categories_field_names + self.FIELD_NAMES_TOP_BOOKS
            )

            for index, row in enumerate(final_rank_rows):
                # TODO: If a sub-category is directly scraped -> all parent categories are currently missing.
                #  They should be included in the csv.
                for level in range(0, deepest_sub_category_level):

                    if level < len(row["category"]):
                        final_rank_rows[index][f"category-{level}"] = row["category"][
                            level
                        ]

                    else:
                        final_rank_rows[index][f"category-{level}"] = ""

                del final_rank_rows[index]["category"]

            fields_for_sorting = ["sales_rank"]
            for level in range(0, deepest_sub_category_level):
                fields_for_sorting.insert(0, f"category-{level}")

            final_rank_rows = sorted(
                final_rank_rows,
                key=lambda x: [x[field] for field in fields_for_sorting],
            )

        except Exception as e:
            LogHandler.log_message(
                f"{self.HEADER} ERROR: An error occurred while trying to sort the product-list. "
                f"Msg: {str(e)}"
            )
            pass

        if category_discovery:
            self.update_categories_tree()

        if self.PRODUCT_LIMIT != 0:
            self.file_handler.write_result_to_csv(
                field_names=self.FIELD_NAMES_TOP_BOOKS,
                rows_for_print=final_rank_rows,
                file_name_prefix=self.product_type,
                file_name_suffix=self.FILE_NAME_SUFFIX_TOP_BOOKS,
            )

    def walk_through_categories(
        self,
        recursive_func,
        browse_nodes,
        final_rank_rows: list,
        categories_list: list = (),
        current_level: int = 0,
    ) -> list:
        for index, node in enumerate(browse_nodes):

            LogHandler.log_message(
                f"{self.HEADER} NODE: {index} C{current_level} {node.name} ({node.id})"
            )

            valid_category_check = False
            # If sub-categories are definied -> ignore selected main-categories
            if self.INCLUDED_MAIN_CATEGORIES[self.product_type] and not self.SPECIFIC_SUB_CATEGORIES[self.product_type]:
                for included_category in self.INCLUDED_MAIN_CATEGORIES[self.product_type]:
                    if included_category in node.name.text or node.name.text in ["Kategorien", "Kindle eBooks"]:
                        # If the category is in the included list -> proceed
                        valid_category_check = True
                        break

                    elif any(included_category in part for part in categories_list):
                        valid_category_check = True

            else:
                valid_category_check = True

            if not valid_category_check:
                print(f"{self.HEADER} NODE: Skipping {node.name.text}")
                continue

            new_categories_list = deepcopy(categories_list)
            new_categories_list.append(f"{node.name.text} [{str(node.id)}]")

            try:
                children_references = node.children

            except AttributeError:
                # If no more children are found - use this node for getting the top-seller-items
                self.categories_paths.append(new_categories_list)

                final_rank_rows = self.fetch_product_details(
                    child_id=node.id,
                    categories_list=new_categories_list,
                    final_rank_rows=final_rank_rows,
                )
                return final_rank_rows

            else:
                for child_reference in children_references:
                    child_nodes = self.api_handler.api_call_with_retry(
                        function=self.api_handler.browse_node_lookup,
                        function_params={"BrowseNodeId": child_reference.id},
                    )

                    if child_nodes:
                        if not self.verbose or node.name.text in ["Wirtschaftskriminalität", "Vampire"]:
                            LogHandler.log_message(
                                f"{self.HEADER} {node.name}: Children: {[i.name for i in child_nodes]}"
                            )

                        new_level = current_level + 1

                        time.sleep(1)

                        final_rank_rows = recursive_func(
                            recursive_func=recursive_func,
                            browse_nodes=child_nodes,
                            categories_list=new_categories_list,
                            final_rank_rows=final_rank_rows,
                            current_level=new_level,
                        )

        return final_rank_rows

    def fetch_product_details(
        self, final_rank_rows, child_id, categories_list: list = ()
    ) -> list:

        if self.PRODUCT_LIMIT == 0:
            return final_rank_rows

        products = self.api_handler.api_call_with_retry(
            function=self.api_handler.browse_node_lookup,
            function_params={"BrowseNodeId": child_id, "ResponseGroup": "TopSellers"},
        )

        for product_index, product in enumerate(products):
            root = ET.fromstring(product.to_string())
            top_seller_items = root.findall(
                ".//owl:TopSellers/owl:TopSeller",
                namespaces=self.api_handler.AMAZON_NAMESPACE,
            )

            for item_index, item in enumerate(top_seller_items):
                if item_index == self.PRODUCT_LIMIT:
                    break

                title = item.find(
                    "owl:Title", namespaces=self.api_handler.AMAZON_NAMESPACE
                )
                asin = item.find(
                    "owl:ASIN", namespaces=self.api_handler.AMAZON_NAMESPACE
                )

                if asin is None:
                    continue
                else:
                    asin = asin.text

                if title is not None:
                    title = title.text

                try:
                    product_sales_rank = self.api_handler.api_call_with_retry(
                        function=self.api_handler.lookup,
                        function_params={
                            "ItemId": asin,
                            "Power": "binding:paperback",
                            "ResponseGroup": "SalesRank",
                        },
                    )

                    sales_rank = product_sales_rank.sales_rank
                    offer_url = product_sales_rank.offer_url

                except Exception as e:
                    LogHandler.log_message(
                        f"{self.HEADER} ERROR: Could not fetch sales_rank for ASIN {asin}! Msg: {str(e)}"
                    )

                    sales_rank = 0
                    offer_url = "N/A"

                row = {
                    "category": categories_list,
                    "asin": asin,
                    "title": title,
                    "sales_rank": int(sales_rank),
                    "offer_url": offer_url,
                }

                final_rank_rows.append(row)

                if self.verbose:
                    LogHandler.log_message(f"{self.HEADER}: Current-Row: {row}")
                else:
                    LogHandler.log_message(f"{self.HEADER}: Found-Book: {row['title']}")

        return final_rank_rows

    def update_categories_tree(self) -> None:

        # Create new categories-tree
        for path in self.categories_paths:
            # print(path)
            current_level = self.category_tree

            for part in path:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

        # update the original file (no deletions)
        def update_orig_categories_dict(recursive_func: Callable, orig_dict: dict, new_dict: dict):
            for key, value in new_dict.items():
                if key not in orig_dict.keys():
                    orig_dict[key] = value
                else:
                    if value:
                        orig_dict[key] = recursive_func(
                            recursive_func, orig_dict[key], new_dict[key]
                        )
            return orig_dict

        file_name = self.get_categories_tree_file_name(product_type=self.product_type)

        orig_discovered_categories = self.file_handler.read_categories_tree_file(
            file_name=file_name
        )

        new_categories_tree = update_orig_categories_dict(
            recursive_func=update_orig_categories_dict,
            orig_dict=orig_discovered_categories,
            new_dict=self.category_tree,
        )

        self.file_handler.update_categories_tree_file(
            file_name=file_name,
            categories_tree=new_categories_tree,
        )

    @classmethod
    def get_categories_tree_file_name(cls, product_type: str):
        return product_type + "_" + cls.FILE_NAME_SUFFIX_CATEGORIES_TREE

    @classmethod
    def get_categories_tree_json_elements(cls, categories_json: dict, format_values: bool = True) -> list:
        tree_json_elements = []
        space = '  '

        def walk_entire_dict(d: dict, n: int = 0):
            row_sign = f"{n}|"
            for key, values in d.items():

                if format_values:
                    if '[' in key:
                        key_split = key.split('[')
                    else:
                        key_split = key.split('[') + [']']

                    new_label = "{:55s}".format(f"{space * n}{row_sign} {key_split[0][:-1]}")
                    tree_json_elements.append(f"{new_label}[{key_split[1]}\n")
                else:
                    tree_json_elements.append(key)

                if isinstance(values, dict):
                    walk_entire_dict(values, n + 1)

                else:
                    if format_values:
                        values_split = values.split('[')
                        new_label = "{:75s}".format(f"{space * n}{row_sign} {values_split[0][:-1]}")
                        tree_json_elements.append(f"{new_label}[{values_split[1]}\n")
                    else:
                        tree_json_elements.append(values)

        walk_entire_dict(categories_json, 0)

        if format_values:
            for index, row in enumerate(tree_json_elements):
                row_nr = "{:4s}".format(str(index + 1))
                tree_json_elements[index] = f"{row_nr} {row}"

        return tree_json_elements

    @classmethod
    def reconvert_category_label_from_formatted_to_raw_value(
            cls, selected_sub_categories_labels: list, file_handler, product_type: str
    ) -> list:
        selected_sub_categories_full_name_list = []

        file_name = cls.get_categories_tree_file_name(product_type=product_type)

        categories_json = file_handler.read_categories_tree_file(file_name=file_name)

        categories_list = cls.get_categories_tree_json_elements(categories_json=categories_json, format_values=False)

        for full_category_name in categories_list:
            for formatted_selected_category in selected_sub_categories_labels:
                selected_categ_without_list_sign = formatted_selected_category.split('|')[1][1:]  # remove sign at front
                selected_category_label = selected_categ_without_list_sign.split('[')[0]  # get only label (no id)
                selected_category_id = "[" + selected_categ_without_list_sign.split('[')[1].replace('\n', '')  # get id part
                selected_category_label = selected_category_label.rstrip()  # Remove padding white space
                selected_category = selected_category_label + " " + selected_category_id  # rejoin in correct format

                if selected_category == full_category_name:
                    selected_sub_categories_full_name_list.append(full_category_name)

        return selected_sub_categories_full_name_list
