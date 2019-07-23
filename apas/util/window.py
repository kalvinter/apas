import PySimpleGUI as sg
from apas.util.logging import LogHandler


class WindowManager:
    HEADER = "(WindowManager)"

    FONT = ("Lucida Console", 10)

    MAIN_COLUMN_WIDTH = 85
    MAIN_COLUMN_SIZE = (MAIN_COLUMN_WIDTH, 2)
    OUTPUT_COLUMN_SIZE = (MAIN_COLUMN_WIDTH - 10, 40)

    BUTTON_MENU_MARGIN = (15, 1)
    BUTTON_MENU_MAIN_BUTTON_MARGIN = (10, 1)
    FORM_MARGIN = (0, 1)
    FORM_MARGIN_FRAMES = (25, 1)

    ACTION_BUTTON_MARGIN_LEFT = (0, 1)
    ACTION_BUTTON_MARGIN_CENTER = (10, 2)

    COLOR_SUCCESS = ("white", "green")
    COLOR_ORANGE = ("black", "orange")
    COLOR_NEUTRAL = ""

    main_menu_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Frame(
                title="Run Top-Products-Scraper",
                layout=[[
                    sg.Column(layout=[
                        [
                            sg.Text("", size=(5, 1)),
                            sg.Button(
                                "Start 'Books' Scraper",
                                size=(25, 2),
                                button_color=COLOR_SUCCESS,
                                key="run_scraper_books",
                            ),
                            sg.Text("", size=(2, 1)),
                        ],
                        [
                            sg.Text("", size=(8, 1)),
                            sg.Button(
                                "Change Book Settings",
                                size=(20, 1),
                                button_color=COLOR_NEUTRAL,
                                key="change_settings_books",
                            ),
                            sg.Text("", size=(3, 1)),
                        ],
                        [
                            sg.Text("", size=(8, 1)),
                            sg.Button(
                                "Discovered Categories",
                                size=(20, 1),
                                button_color=COLOR_NEUTRAL,
                                key="show_categories_books",
                            ),
                            sg.Text("", size=(3, 1)),
                        ]
                    ]),
                    sg.VerticalSeparator(pad=None),
                    sg.Column(layout=[
                        [
                            sg.Text("", size=(2, 1)),
                            sg.Button(
                                "Start 'Kindle-E-Books' Scraper",
                                size=(25, 2),
                                button_color=COLOR_SUCCESS,
                                key="run_scraper_kindle_books",
                            ),
                        ],
                        [
                            sg.Text("", size=(4, 1)),
                            sg.Button(
                                "Change E-Book Settings",
                                size=(20, 1),
                                button_color=COLOR_NEUTRAL,
                                key="change_settings_kindle_books",
                            ),
                        ],
                        [
                            sg.Text("", size=(4, 1)),
                            sg.Button(
                                "Discovered Categories",
                                size=(20, 1),
                                button_color=COLOR_NEUTRAL,
                                key="show_categories_kindle_books",
                            ),
                        ]
                    ])
                ]]
            )
        ],
        [
            sg.Text("", size=MAIN_COLUMN_SIZE),

        ],
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Frame(
                title="General Settings",
                layout=[
                    [
                        sg.Text("", size=BUTTON_MENU_MARGIN),
                        sg.Button("Change API Secrets", size=(40, 1), key="change_secrets"),
                        sg.Text("", size=BUTTON_MENU_MARGIN),
                    ],
                    [
                        sg.Text("", size=BUTTON_MENU_MARGIN),
                        sg.Button("Change Main Settings", size=(40, 1), key="change_config"),
                        sg.Text("", size=BUTTON_MENU_MARGIN),
                    ],
                ]

            )
        ],
    ]

    change_main_config_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text("Nr. of Retries: ", size=(30, 1)),
            sg.Spin(values=[i for i in range(0, 11)], size=(40, 1), key="RETRY_LIMIT"),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "This integer-value determines how many times the programme will re-attempt to call the API before "
                "aborting. It should not be set below 3.",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [sg.Text("", size=FORM_MARGIN)],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text("Seconds between Retries: ", size=(30, 1)),
            sg.Spin(
                values=[i for i in range(0, 11)],
                size=(40, 1),
                key="COOLDOWN_TIME_FOR_RETRY",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "This integer-value determines how long the programme will wait in seconds before re-attempting "
                "to call the API. It should not be set below 2.",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [sg.Text("", size=FORM_MARGIN)],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text("Verbosity-Level: ", size=(30, 1)),
            sg.Combo(
                values=["Empty"], size=(40, 1), key="VERBOSE_OUTPUT", readonly=True
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "When this is set to 'Detailed', the information output on the left will include more and more "
                "detailled messages. You need to restart the application for a change in this setting "
                "to take effect.",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [sg.Text("", size=FORM_MARGIN)],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text("Nr. of Fetched Products: ", size=(30, 1)),
            sg.InputText(size=(40, 1), key="PRODUCT_LIMIT"),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "This integer-value determines how many products and Bestseller-Scores will be fetched per "
                "category. If it is set to 0 then no products are fetched. This is useful for discovering "
                "categories or simply testing if the application",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [sg.Text("", size=(MAIN_COLUMN_WIDTH, 10))],
        [
            sg.Text("", size=ACTION_BUTTON_MARGIN_LEFT),
            sg.Button(
                "Cancel",
                size=(30, 2),
                button_color=COLOR_ORANGE,
                key="cancel_edit_config",
            ),
            sg.Text("", size=ACTION_BUTTON_MARGIN_CENTER),
            sg.Button(
                "Save new Config-Values",
                size=(30, 2),
                button_color=COLOR_SUCCESS,
                key="save_config",
            ),
        ],
    ]

    books_included_categories_col = [
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Listbox(
                values=(["Empty"]),
                key="books_included_main_categories",
                size=(34, 27),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                default_values=[],
                font=FONT,
            ),
        ],
        [
            sg.Button(button_text="Deselect all", button_color=("black", "white"),
                      size=(35, 1), key="deselect_all_books_included_main_categories")
        ],
        [sg.Text("", key="books_included_main_categories_nr", text_color="grey", size=(35, 1))]
    ]

    books_specific_sub_categories_col = [
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Listbox(
                values=(["Empty"]),
                key="books_specific_sub_categories",
                size=(33, 27),
                font=FONT,
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                default_values=[],
            ),
        ],
        [
            sg.Button(button_text="Deselect all", button_color=("black", "white"),
                      size=(35, 1), key="deselect_all_books_specific_sub_categories")
        ],
        [sg.Text("", key="books_specific_sub_categories_nr", text_color="grey", size=(35, 1))]
    ]

    change_settings_books_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Frame(
                title="Select one or more MAIN-Categories for scraping",
                layout=books_included_categories_col,
            ),
            sg.Frame(
                title="OR Select specific SUB-Categories for scraping",
                layout=books_specific_sub_categories_col,
            ),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "NOTE: The sub-categories are discovered by scraping the associated MAIN-category! The more MAIN-"
                "categories you have scraped, the more sub-categories you will be able to select.",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=ACTION_BUTTON_MARGIN_LEFT),
            sg.Button(
                "Cancel",
                button_color=COLOR_ORANGE,
                size=(30, 2),
                key="cancel_edit_settings_books",
            ),
            sg.Text("", size=ACTION_BUTTON_MARGIN_CENTER),
            sg.Button(
                "Save", button_color=COLOR_SUCCESS, size=(30, 2), key="save_settings_books"
            ),
        ],
    ]

    kindle_books_included_categories_col = [
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Listbox(
                values=(["Empty"]),
                key="kindle_books_included_main_categories",
                size=(34, 27),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                default_values=[],
                font=FONT
            ),
        ],
        [
            sg.Button(button_text="Deselect all", button_color=("black", "white"),
                      size=(35, 1), key="deselect_all_kindle_books_included_main_categories")
        ],
        [sg.Text("", key="kindle_books_included_main_categories_nr", text_color="grey", size=(35, 1))]
    ]

    kindle_books_specific_sub_categories_col = [
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Listbox(
                values=(["Empty"]),
                key="kindle_books_specific_sub_categories",
                size=(33, 27),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                default_values=[],
                font=FONT
            ),
        ],
        [
            sg.Button(button_text="Deselect all", button_color=("black", "white"),
                      size=(35, 1), key="deselect_all_kindle_books_specific_sub_categories")
        ],
        [sg.Text("", key="kindle_books_specific_sub_categories_nr", text_color="grey", size=(35, 1))]
    ]

    change_settings_kindle_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Frame(
                title="Select one or more MAIN-Categories for scraping",
                layout=kindle_books_included_categories_col,
            ),
            sg.Frame(
                title="OR Select specific SUB-Categories for scraping",
                layout=kindle_books_specific_sub_categories_col,
            ),
        ],
        [
            sg.Text("", size=FORM_MARGIN),
            sg.Text(
                "NOTE: The sub-categories are discovered by scraping the associated MAIN-category! The more MAIN-"
                "categories you have scraped, the more sub-categories you will be able to select.",
                size=(70, 2),
                text_color="grey",
            ),
            sg.Text("", size=FORM_MARGIN),
        ],
        [
            sg.Text("", size=ACTION_BUTTON_MARGIN_LEFT),
            sg.Button(
                "Cancel",
                button_color=COLOR_ORANGE,
                size=(30, 2),
                key="cancel_edit_settings_kindle_books",
            ),
            sg.Text("", size=ACTION_BUTTON_MARGIN_CENTER),
            sg.Button(
                "Save", button_color=COLOR_SUCCESS, size=(30, 2), key="save_settings_kindle_books"
            ),
        ],
    ]

    change_secrets_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=FORM_MARGIN_FRAMES),
            sg.Frame(
                title="Amazon Access Key",
                layout=[[sg.InputText(key="AMAZON_ACCESS_KEY", size=(30, 15), password_char='*')]],
            ),
            sg.Text("", size=FORM_MARGIN_FRAMES),
        ],
        [
            sg.Text("", size=FORM_MARGIN_FRAMES),
            sg.Frame(
                title="Amazon Secret Key",
                layout=[[sg.InputText(key="AMAZON_SECRET_KEY", size=(30, 15), password_char='*')]],
            ),
            sg.Text("", size=FORM_MARGIN_FRAMES),
        ],
        [
            sg.Text("", size=FORM_MARGIN_FRAMES),
            sg.Frame(
                title="Amazon Association Tag",
                layout=[[sg.InputText(key="AMAZON_ASSOC_TAG", size=(30, 15), password_char='*')]],
            ),
            sg.Text("", size=FORM_MARGIN_FRAMES),
        ],
        [sg.Text("", key="secrets_message", size=(75, 1), text_color="red")],
        [sg.Text("", size=(MAIN_COLUMN_WIDTH, 20))],
        [
            sg.Text("", size=ACTION_BUTTON_MARGIN_LEFT),
            sg.Button(
                "Cancel", button_color=COLOR_ORANGE, size=(30, 2), key="cancel_change_secrets"
            ),
            sg.Text("", size=ACTION_BUTTON_MARGIN_CENTER),
            sg.Button(
                "Save", button_color=COLOR_SUCCESS, size=(30, 2), key="save_secrets"
            ),
        ],
    ]

    show_category_tree_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE, key="categories_error_message", text_color="red")],
        [
            sg.Multiline(default_text="", key="categories_tree_field", enter_submits=False, enable_events=False,
                         size=(40, 35), font=FONT)
         ],
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=ACTION_BUTTON_MARGIN_LEFT),
            sg.Button(
                "Menu", button_color=COLOR_ORANGE, size=(30, 2), key="cancel_show_categories"
            ),
        ],
    ]

    run_scraper_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Text("Runnning Amazon-Top-Products-Scraper ..."),
        ],
    ]

    run_scraper_success_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Text("Finished running Amazon-Top-Products-Scraper!"),
        ],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Button("Back to Menu", size=(30, 2), key="success_back_to_menu"),
        ],
    ]

    run_scraper_failure_col = [
        [sg.Text("", size=MAIN_COLUMN_SIZE)],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Text("An error occurred while runnning Amazon-Top-Products-Scraper!"),
        ],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Text(
                "Please copy the text in the left box into a file and send it to the developer."
            ),
        ],
        [
            sg.Text("", size=BUTTON_MENU_MARGIN),
            sg.Button("Back to Menu", size=(30, 2), key="failure_back_to_menu"),
        ],
    ]

    layout_main_window = [
        [
            sg.Output(size=OUTPUT_COLUMN_SIZE),
            sg.Column(main_menu_col, key="main_menu_col"),
            sg.Column(
                change_main_config_col, key="change_main_config_col", visible=False
            ),
            sg.Column(
                change_settings_books_col, key="change_settings_books_col", visible=False
            ),
            sg.Column(
                change_settings_kindle_col, key="change_settings_kindle_col", visible=False
            ),
            sg.Column(
                change_secrets_col, key="change_secrets_col", visible=False
            ),
            sg.Column(
                show_category_tree_col, key="show_category_tree_col", visible=False
            ),
            sg.Column(
                run_scraper_col, key="run_scraper_col", visible=False
            ),
            sg.Column(
                run_scraper_success_col, key="run_scraper_success_col", visible=False
            ),
            sg.Column(
                run_scraper_failure_col, key="run_scraper_failure_col", visible=False
            ),
        ]
    ]

    main_window = None

    def __init__(self, node_crawler_class, config_handler, file_handler):
        self.config_handler = config_handler
        self.config_dict = config_handler.config_dict
        self.secrets_dict = config_handler.secrets_dict
        self.node_crawler_class = node_crawler_class
        self.file_handler = file_handler

    def open_window(self, window_name: str):
        self.main_window = sg.Window(
            window_name, self.layout_main_window, auto_close=False, use_default_focus=False,
        )
        self.main_window.Finalize()
        self.refresh_values_in_forms()
        return self.main_window

    def refresh_values_in_forms(self):
        self.config_dict = self.config_handler.config_dict
        # ---- Pre-Fill config-form ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
        self.main_window.FindElement("RETRY_LIMIT").Update(
            value=self.config_dict["RETRY_LIMIT"]
        )

        self.main_window.FindElement("COOLDOWN_TIME_FOR_RETRY").Update(
            value=self.config_dict["COOLDOWN_TIME_FOR_RETRY"]
        )

        verbosity_options_list = list(self.config_handler.VERBOSITY_OPTIONS.keys())
        self.main_window.FindElement("VERBOSE_OUTPUT").Update(
            values=verbosity_options_list
        )

        self.main_window.FindElement("PRODUCT_LIMIT").Update(
            value=self.config_dict["PRODUCT_LIMIT"]
        )

        verbosity_level = self.config_dict["VERBOSE_OUTPUT"]
        for key, value in self.config_handler.VERBOSITY_OPTIONS.items():
            if verbosity_level == value:
                verbosity_level = key
        try:
            self.main_window.FindElement("VERBOSE_OUTPUT").Update(
                set_to_index=verbosity_options_list.index(verbosity_level)
            )
        except (IndexError, ValueError) as e:
            LogHandler.log_message(e)

        # ---- Pre-Fill secrets-page ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
        self.main_window.FindElement('AMAZON_ACCESS_KEY').Update(
            value=self.secrets_dict['AMAZON_ACCESS_KEY']
        )

        self.main_window.FindElement('AMAZON_SECRET_KEY').Update(
            value=self.secrets_dict['AMAZON_SECRET_KEY']
        )

        self.main_window.FindElement('AMAZON_ASSOC_TAG').Update(
            value=self.secrets_dict['AMAZON_ASSOC_TAG']
        )

        # ---- Pre-Fill settings-books ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
        self.main_window.FindElement("books_included_main_categories").Update(
            values=self.node_crawler_class.MAIN_CATEGORIES['books'], set_to_index=-1
        )

        included_main_categories = self.config_dict["BrowseNodeCrawler"]['books']["INCLUDED_MAIN_CATEGORIES"]

        self.main_window.FindElement('books_included_main_categories_nr').Update(
            value=f"Currently Saved: {len(included_main_categories)} selected"
        )

        for item in included_main_categories:
            self.main_window.FindElement("books_included_main_categories").Update(
                set_to_index=self.node_crawler_class.MAIN_CATEGORIES['books'].index(item)
            )

        file_name = self.node_crawler_class.get_categories_tree_file_name(product_type="books")
        categories_json = self.file_handler.read_categories_tree_file(file_name=file_name)

        if categories_json:
            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json=categories_json
            )

            self.main_window.FindElement("books_specific_sub_categories").Update(
                values=discovered_sub_categories, set_to_index=-1
            )

            specific_sub_categories = self.config_dict["BrowseNodeCrawler"]['books']["SPECIFIC_SUB_CATEGORIES"]

            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json, format_values=False
            )

            for item in specific_sub_categories:
                try:
                    self.main_window.FindElement("books_specific_sub_categories").Update(
                        set_to_index=discovered_sub_categories.index(item)
                    )
                except (IndexError, ValueError):
                    pass

            self.main_window.FindElement('books_specific_sub_categories_nr').Update(
                value=f"Currently Saved: {len(specific_sub_categories)} selected"
            )

        else:
            self.main_window.FindElement("books_specific_sub_categories").Update(
                values=[], set_to_index=-1
            )
            self.main_window.FindElement('books_specific_sub_categories_nr').Update(
                value=f"No categories discovered yet"
            )

        # ---- Pre-Fill settings-kindle ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
        self.main_window.FindElement("kindle_books_included_main_categories").Update(
            values=self.node_crawler_class.MAIN_CATEGORIES['kindle_books'], set_to_index=-1
        )

        included_main_categories = self.config_dict["BrowseNodeCrawler"]['kindle_books']["INCLUDED_MAIN_CATEGORIES"]

        self.main_window.FindElement('kindle_books_included_main_categories_nr').Update(
            value=f"Currently Saved: {len(included_main_categories)} selected"
        )

        for item in included_main_categories:
            self.main_window.FindElement("kindle_books_included_main_categories").Update(
                set_to_index=self.node_crawler_class.MAIN_CATEGORIES['kindle_books'].index(item)
            )

        file_name = self.node_crawler_class.get_categories_tree_file_name(product_type="kindle_books")
        categories_json = self.file_handler.read_categories_tree_file(file_name=file_name)

        if categories_json:
            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json=categories_json
            )

            self.main_window.FindElement("kindle_books_specific_sub_categories").Update(
                values=discovered_sub_categories, set_to_index=-1
            )

            specific_sub_categories = self.config_dict["BrowseNodeCrawler"]['kindle_books']["SPECIFIC_SUB_CATEGORIES"]

            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json, format_values=False
            )

            for item in specific_sub_categories:
                try:
                    self.main_window.FindElement("kindle_books_specific_sub_categories").Update(
                        set_to_index=discovered_sub_categories.index(item)
                    )
                except (IndexError, ValueError):
                    pass

            self.main_window.FindElement('kindle_books_specific_sub_categories_nr').Update(
                value=f"Currently Saved: {len(specific_sub_categories)} selected"
            )

        else:
            self.main_window.FindElement("kindle_books_specific_sub_categories").Update(
                values=[], set_to_index=-1
            )
            self.main_window.FindElement('kindle_books_specific_sub_categories_nr').Update(
                value=f"No categories discovered yet"
            )

    def switch_to_main_menu(self):
        self.main_window.FindElement("main_menu_col").Update(visible=True)
        self.main_window.FindElement("change_main_config_col").Update(visible=False)
        self.main_window.FindElement("change_settings_books_col").Update(visible=False)
        self.main_window.FindElement("change_settings_kindle_col").Update(visible=False)
        self.main_window.FindElement("show_category_tree_col").Update(visible=False)
        self.main_window.FindElement("change_secrets_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_success_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_failure_col").Update(visible=False)
        self.update_window()

    def switch_to_change_config(self):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Change Config'-Section"
        )
        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("change_main_config_col").Update(visible=True)
        self.update_window()

    def switch_to_change_settings_books(self):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Change Settings Books'-Section"
        )
        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("change_settings_books_col").Update(visible=True)
        self.update_window()

    def deselect_all_books_included_main_categories(self):
        self.main_window.FindElement("books_included_main_categories").Update(
            values=self.node_crawler_class.MAIN_CATEGORIES['books'], set_to_index=-1
        )
        self.update_window()

    def deselect_all_books_specific_sub_categories(self):
        file_name = self.node_crawler_class.get_categories_tree_file_name(product_type="books")
        categories_json = self.file_handler.read_categories_tree_file(file_name=file_name)

        if categories_json:
            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json=categories_json
            )

            self.main_window.FindElement("books_specific_sub_categories").Update(
                values=discovered_sub_categories, set_to_index=-1
            )
        else:
            self.main_window.FindElement("books_specific_sub_categories").Update(
                values=[], set_to_index=-1
            )
        self.update_window()

    def switch_to_change_settings_kindle(self):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Change Settings E-Books'-Section"
        )
        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("change_settings_kindle_col").Update(visible=True)
        self.update_window()

    def deselect_all_kindle_books_included_main_categories(self):
        self.main_window.FindElement("kindle_books_included_main_categories").Update(
            values=self.node_crawler_class.MAIN_CATEGORIES['kindle_books'], set_to_index=-1
        )
        self.update_window()

    def deselect_all_kindle_books_specific_sub_categories(self):
        file_name = self.node_crawler_class.get_categories_tree_file_name(product_type="kindle_books")
        categories_json = self.file_handler.read_categories_tree_file(file_name=file_name)

        if categories_json:
            discovered_sub_categories = self.node_crawler_class.get_categories_tree_json_elements(
                categories_json=categories_json
            )

            self.main_window.FindElement("kindle_books_specific_sub_categories").Update(
                values=discovered_sub_categories, set_to_index=-1
            )
        else:
            self.main_window.FindElement("kindle_books_specific_sub_categories").Update(
                values=[], set_to_index=-1
            )
        self.update_window()

    def switch_to_change_secrets(self, secrets_empty: bool = False):
        if secrets_empty:
            LogHandler.log_message(
                f"{self.HEADER}: Could not find secrets in secrets.json!"
            )
            self.main_window.FindElement('secrets_message').Update(
                value="                          Please enter your secret-values. Otherwise the app will not be able "
                      "to use the API!"
            )
            self.main_window.FindElement('cancel_change_secrets').Update(visible=False)
        else:
            self.main_window.FindElement('secrets_message').Update(
                value=""
            )
            self.main_window.FindElement('cancel_change_secrets').Update(visible=True)

        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Change Secrets'-Section"
        )
        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("change_secrets_col").Update(visible=True)
        self.update_window()

    def switch_to_show_category_tree(self, product_type: str):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Show Categories"
        )
        file_name = self.node_crawler_class.get_categories_tree_file_name(product_type=product_type)
        categories_json = self.file_handler.read_categories_tree_file(file_name=file_name)

        if categories_json:
            tree_json_elements = self.node_crawler_class.get_categories_tree_json_elements(categories_json)
            tree_json_str = ''.join(tree_json_elements)
            # print(tree_json_str)
            self.main_window.FindElement("categories_error_message").Update(
                value=""
            )
            self.main_window.FindElement("categories_tree_field").Update(
                value=tree_json_str
            )

        else:
            tree_json_str = "No categories have been discovered yet. Please run the scraper first. All discovered " \
                            "categories will be saved here."

            self.main_window.FindElement("categories_error_message").Update(
                value=tree_json_str
            )

        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("show_category_tree_col").Update(visible=True)

    def switch_to_run_scraper(self):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Run-Top-Products-Scraper'-Section"
        )
        self.main_window.FindElement("main_menu_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_col").Update(visible=True)
        self.update_window()

    def switch_to_run_scraper_success(self):
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Run-Top-Products-Scraper-Success'-Section"
        )
        self.main_window.FindElement("run_scraper_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_success_col").Update(visible=True)
        self.update_window()

    def switch_to_run_scraper_failure(self, error_message: str):
        LogHandler.log_message(
            f"{self.HEADER}: ERROR: The following error occurred while trying to run the scraper: '{error_message}'."
        )
        LogHandler.log_message(
            f"{self.HEADER}: Changing window to 'Run-Top-Products-Scraper-Failure'-Section"
        )
        self.main_window.FindElement("run_scraper_col").Update(visible=False)
        self.main_window.FindElement("run_scraper_failure_col").Update(visible=True)
        self.update_window()

    def update_window(self):
        self.main_window.Refresh()
        self.main_window.Size = self.main_window.Size
