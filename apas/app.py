from apas.features import node_crawler_feature
from apas.util import window, logging, api, config, files, startup


PROGRAMME_NAME = "Amazon-Product-API Scraper (APAS)"
HEADER = "(MAIN)"


def run():
    start_up_handler = startup.StartUpHandler(verbose=True)

    config_handler = config.ConfigHandler(start_up_handler=start_up_handler)
    config_handler.load_config_from_file()
    config_handler.load_secrets_from_file()
    verbose = config_handler.config_dict["VERBOSE_OUTPUT"]

    file_handler = files.FileHandler(start_up_handler=start_up_handler, verbose=verbose)
    log_handler = logging.LogHandler

    window_manager = window.WindowManager(
        node_crawler_class=node_crawler_feature.BrowseNodeCrawler,
        config_handler=config_handler, file_handler=file_handler
    )
    main_window = window_manager.open_window(window_name=PROGRAMME_NAME)

    log_handler.set_output_target(
        standard_stdout=False, window=True, main_window_instance=main_window
    )

    start_up_handler.print_start_up_messages()
    print(f"{start_up_handler.HEADER} [OK] Successfully loaded config-files.")

    api_handler = api.APIHandler(
        verbose=verbose
    )

    if config_handler.secrets_dict_is_empty():
        window_manager.switch_to_change_secrets(secrets_empty=True)

    while True:
        event, values = main_window.Read()

        if verbose:
            print(event, values)

        if event is None or event == "Exit":
            break

        elif event == "change_secrets":
            window_manager.switch_to_change_secrets()

        elif event == "save_secrets":
            window_manager.switch_to_main_menu()

            new_secrets_dict = {
                "AMAZON_ACCESS_KEY": values["AMAZON_ACCESS_KEY"],
                "AMAZON_SECRET_KEY": values["AMAZON_SECRET_KEY"],
                "AMAZON_ASSOC_TAG": values["AMAZON_ASSOC_TAG"],
            }

            config_handler.update_secrets_file(new_secrets_dict=new_secrets_dict)
            config_handler.load_secrets_from_file()

        elif event in ["cancel_change_secrets", "cancel_edit_config", "cancel_edit_settings_books",
                       "cancel_edit_settings_kindle_books", "cancel_show_categories"]:
            window_manager.refresh_values_in_forms()
            window_manager.refresh_values_in_forms()
            window_manager.switch_to_main_menu()

        elif event == "change_config":
            config_handler.load_config_from_file()
            window_manager.switch_to_change_config()

        elif event == "save_config":
            window_manager.switch_to_main_menu()

            try:
                values["RETRY_LIMIT"] = int(values["RETRY_LIMIT"])
                values["COOLDOWN_TIME_FOR_RETRY"] = int(values["COOLDOWN_TIME_FOR_RETRY"])
                values["PRODUCT_LIMIT"] = int(values["PRODUCT_LIMIT"])

                new_config_dict = {
                    "RETRY_LIMIT": values["RETRY_LIMIT"],
                    "COOLDOWN_TIME_FOR_RETRY": values["COOLDOWN_TIME_FOR_RETRY"],
                    "VERBOSE_OUTPUT": values["VERBOSE_OUTPUT"],
                    "PRODUCT_LIMIT": values["PRODUCT_LIMIT"],
                }
                config_handler.update_config_file(new_config_dict=new_config_dict)

            except ValueError as e:
                print(
                    f"{HEADER} ERROR: Invalid value received. Must be an integer! Msg.: {str(e)}"
                )

            config_handler.load_config_from_file()
            window_manager.refresh_values_in_forms()

        elif event == "change_settings_books":
            window_manager.switch_to_change_settings_books()

        elif event == "deselect_all_books_included_main_categories":
            window_manager.deselect_all_books_included_main_categories()

        elif event == 'deselect_all_books_specific_sub_categories':
            window_manager.deselect_all_books_specific_sub_categories()

        elif event == "save_settings_books":
            window_manager.switch_to_main_menu()

            books_specific_sub_categories = node_crawler_feature.BrowseNodeCrawler\
                .reconvert_category_label_from_formatted_to_raw_value(
                    selected_sub_categories_labels=values["books_specific_sub_categories"],
                    file_handler=file_handler, product_type="books"
            )

            new_config_dict = {
                "BrowseNodeCrawler": {
                    "books": {
                        "INCLUDED_MAIN_CATEGORIES": values["books_included_main_categories"],
                        "SPECIFIC_SUB_CATEGORIES": books_specific_sub_categories,
                    }
                }
            }

            config_handler.update_config_file(new_config_dict=new_config_dict)
            config_handler.load_config_from_file()
            window_manager.refresh_values_in_forms()

        elif event == "change_settings_kindle_books":
            window_manager.switch_to_change_settings_kindle()

        elif event == "deselect_all_kindle_books_included_main_categories":
            window_manager.deselect_all_kindle_books_included_main_categories()

        elif event == "deselect_all_kindle_books_specific_sub_categories":
            window_manager.deselect_all_kindle_books_specific_sub_categories()

        elif event == "save_settings_kindle_books":
            window_manager.switch_to_main_menu()

            kindle_books_specific_sub_categories = node_crawler_feature.BrowseNodeCrawler \
                .reconvert_category_label_from_formatted_to_raw_value(
                  selected_sub_categories_labels=values["kindle_books_specific_sub_categories"],
                  file_handler=file_handler, product_type="kindle_books"
            )

            new_config_dict = {
                "BrowseNodeCrawler": {
                    "kindle_books": {
                        "INCLUDED_MAIN_CATEGORIES": values["kindle_books_included_main_categories"],
                        "SPECIFIC_SUB_CATEGORIES": kindle_books_specific_sub_categories,
                    }
                }
            }

            config_handler.update_config_file(new_config_dict=new_config_dict)

            config_handler.load_config_from_file()
            window_manager.refresh_values_in_forms()

        elif event == "show_categories_books":
            window_manager.switch_to_show_category_tree(product_type='books')

        elif event == "show_categories_kindle_books":
            window_manager.switch_to_show_category_tree(product_type='kindle_books')

        elif event == "run_scraper_books" or event == "run_scraper_kindle_books":
            window_manager.switch_to_run_scraper()

            api_handler.create_api_connection(
                config_dict=config_handler.config_dict,
                secrets_dict=config_handler.secrets_dict
            )

            node_crawler = node_crawler_feature.BrowseNodeCrawler(
                api_handler=api_handler,
                file_handler=file_handler,
                config_dict=config_handler.config_dict,
                verbose=verbose,
            )

            try:
                if event == "run_scraper_books":
                    node_crawler.run_crawler(browse_node_id=541686)

                elif event == "run_scraper_kindle_books":
                    node_crawler.run_crawler(browse_node_id=530886031)

                else:
                    raise Exception("ProgrammingError: Invalid event provided for starting the scraper!")

                window_manager.refresh_values_in_forms()
                window_manager.switch_to_run_scraper_success()

            except Exception as e:
                window_manager.switch_to_run_scraper_failure(error_message=str(e))

        elif event == "failure_back_to_menu" or event == "success_back_to_menu":
            window_manager.switch_to_main_menu()

        main_window.Refresh()
        main_window.Size = main_window.Size
