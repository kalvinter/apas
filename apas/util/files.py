from apas.util.logging import LogHandler

from datetime import datetime
import pathlib
import csv
import json
import os


class FileHandler:
    HEADER = "{0: <20}".format("(FileHandler):")
    REQUIRED_FOLDERS = ['data', 'csv_output']

    def __init__(self, start_up_handler,  verbose: bool = False):
        self.start_up_handler = start_up_handler
        self.ROOT_DIR = self.start_up_handler.ROOT_DIR
        self.verbose = verbose

    @staticmethod
    def clean_file_path_variables(path_element: str):
        """Remove / and \\ so that the path-element can be used in a joinpath-operation. The pathlib-library will set
         these chars itself. """
        patterns = ["/", "\\"]

        for pattern in patterns:
            path_element = path_element.replace(pattern, "")

        return path_element

    def write_result_to_csv(
        self, field_names: list, rows_for_print: list, file_name_prefix: str = "", file_name_suffix: str = ".csv"
    ):
        file_name = file_name_prefix + "_" + str(datetime.today().date()) + file_name_suffix
        file_path = pathlib.Path.joinpath(self.ROOT_DIR, "csv_output", file_name)

        LogHandler.log_message(
            f"{self.HEADER} INFO: Start writing results to a new csv-file. File: {file_path}"
        )

        try:
            with open(str(file_path), "w", newline="") as csv_file:
                writer = csv.DictWriter(
                    csv_file, fieldnames=field_names, dialect="excel", delimiter=";"
                )
                writer.writeheader()

                for row in rows_for_print:
                    writer.writerow(row)

        except IOError as e:
            raise Exception(
                f"{self.HEADER}: ERROR: An error occurred while trying to write the results to a new csv. "
                f"Msg.: {str(e)}"
            )

        LogHandler.log_message(
            f"{self.HEADER} INFO: Finished writing results to a new csv-file"
        )

        return 0

    def read_file(self, file_name: str, folder: str) -> str:
        folder = self.clean_file_path_variables(path_element=folder)
        file_name = self.clean_file_path_variables(path_element=file_name)

        file_path = str(pathlib.Path.joinpath(self.ROOT_DIR, folder, file_name))

        if not os.path.isfile(path=file_path):
            try:
                with open(file_path, "w", encoding="UTF-8") as file:
                    file.write("")

            except IOError as e:
                LogHandler.log_message(
                    f"{self.HEADER}: ERROR: Could not find the file {file_path} and tried to create an empty one. "
                    f"An error while trying to create the empty file. Msg.: {str(e)}"
                )

        try:
            with open(file_path, "r") as file:
                content = file.read()

        except IOError as e:
            LogHandler.log_message(
                f"{self.HEADER}: ERROR: An error occurred while trying to read the file {file_path}. Msg.: {str(e)}"
            )
            content = None

        return content

    def update_categories_tree_file(self, categories_tree: dict, file_name: str):
        file_name = self.clean_file_path_variables(path_element=file_name)

        file_path = str(pathlib.Path.joinpath(self.ROOT_DIR, "data", file_name))

        try:
            with open(str(file_path), "w", encoding="UTF-8") as json_file:
                json_file.write(json.dumps(categories_tree))

        except IOError as e:
            print(
                f"{self.HEADER}: ERROR: An error occurred while trying to update "
                f"the discovered-categories-file. Msg.: {str(e)}"
            )
            return 2

        LogHandler.log_message(
            f"{self.HEADER}: INFO: Finished updating the discovered-categories-file"
        )

        return 0

    def read_categories_tree_file(self, file_name: str):
        file_name = self.clean_file_path_variables(path_element=file_name)

        file_path = str(pathlib.Path.joinpath(self.ROOT_DIR, "data", file_name))

        try:
            with open(file_path, "r", encoding="UTF-8") as categories_file:
                try:
                    categories_json = json.loads(categories_file.read(), encoding="UTF-8")

                except json.JSONDecodeError:
                    raise Exception(
                        f"{self.HEADER} ERROR: Could not read File '{file_name}'. Invalid JSON. Please contact"
                        f"the developer."
                    )

        except IOError as e:
            LogHandler.log_message(
                f"{self.HEADER} WARNING: Could not read the original categories-tree-json. "
                f"Creating a new empty categories-tree-json. Msg.: {str(e)}"
            )
            try:
                with open(file_path, "w", encoding="UTF-8") as categories_file:
                    categories_file.write("{}")

            except IOError as e:
                print(
                    f"{self.HEADER}: ERROR: An error occurred while trying to create an empty "
                    f" discovered-categories-file. File name: '{file_name}'. Msg.: {str(e)}"
                )
                return 2

            else:
                categories_json = {}

        return categories_json
