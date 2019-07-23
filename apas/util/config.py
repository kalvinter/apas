from apas.util.logging import LogHandler
import pathlib
import json
import os


class ConfigHandler:
    HEADER = "{0: <20}".format("(ConfigHandler):")
    config_dict = None
    secrets_dict = None

    VERBOSITY_OPTIONS = {"Detailed": True, "Standard": False}

    EMPTY_SECRETS_FILE_CONTENT = {
        "AMAZON_ACCESS_KEY": "",
        "AMAZON_SECRET_KEY": "",
        "AMAZON_ASSOC_TAG": "",
    }

    DEFAULT_CONFIG_FILE_CONTENT = {
        "RETRY_LIMIT": 3,
        "COOLDOWN_TIME_FOR_RETRY": 5,
        "VERBOSE_OUTPUT": "Standard",
        "PRODUCT_LIMIT": 5,
        "BrowseNodeCrawler": {
            "books": {
                "INCLUDED_MAIN_CATEGORIES": [],
                "SPECIFIC_SUB_CATEGORIES": []
            },
            "kindle_books": {
                "INCLUDED_MAIN_CATEGORIES": [],
                "SPECIFIC_SUB_CATEGORIES": []
            }
        }
    }

    ROOT_DIR = None
    CONFIG_FILE_PATH = None
    SECRETS_FILE_PATH = None

    def __init__(self, start_up_handler):
        self.start_up_handler = start_up_handler
        self.ROOT_DIR = self.start_up_handler.ROOT_DIR
        self.CONFIG_FILE_PATH = str(pathlib.Path.joinpath(self.ROOT_DIR, "config", "config.json"))
        self.SECRETS_FILE_PATH = str(pathlib.Path.joinpath(self.ROOT_DIR, "config", "secrets.json"))

    def load_config_from_file(self):
        if not os.path.isfile(self.CONFIG_FILE_PATH):

            msg = f"{self.HEADER} Could not find config.json-File. Creating a new config.json with default values."
            if self.start_up_handler.in_start_up_phase():
                self.start_up_handler.log_start_up_message(msg=msg)
            else:
                print(msg)

            with open(self.CONFIG_FILE_PATH, "w", encoding="UTF-8") as config_file:
                try:
                    config_file.write(json.dumps(self.DEFAULT_CONFIG_FILE_CONTENT))

                except (IOError, json.JSONDecodeError) as e:
                    raise Exception(
                        f"{self.HEADER} ERROR: An error occurred while trying to create a new empty config.json-file! "
                        f"Msg: {str(e)}"
                    )

        with open(self.CONFIG_FILE_PATH, "r", encoding="UTF-8") as config_file:
            try:
                self.config_dict = json.loads(config_file.read(), encoding="UTF-8")

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: Config.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

            try:
                self.config_dict["VERBOSE_OUTPUT"] = self.VERBOSITY_OPTIONS[
                    self.config_dict["VERBOSE_OUTPUT"]
                ]
            except KeyError:
                self.config_dict["VERBOSE_OUTPUT"] = False

    def load_secrets_from_file(self):
        if not os.path.isfile(self.SECRETS_FILE_PATH):

            msg = f"{self.HEADER} Could not find config.json-File. Creating a new secrets.json with empty values."
            if self.start_up_handler.in_start_up_phase():
                self.start_up_handler.log_start_up_message(msg=msg)
            else:
                print(msg)

            with open(self.SECRETS_FILE_PATH, "w", encoding="UTF-8") as new_secrets_file:
                try:
                    new_secrets_file.write(json.dumps(self.EMPTY_SECRETS_FILE_CONTENT))

                except IOError:
                    raise Exception(
                        f"{self.HEADER} ERROR: Could not create a new empty secrets.json-file!"
                    )

        with open(self.SECRETS_FILE_PATH, "r", encoding="UTF-8") as secrets_file:
            try:
                self.secrets_dict = json.loads(secrets_file.read(), encoding="UTF-8")

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: Config.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

    def secrets_dict_is_empty(self):
        for key, value in self.secrets_dict.items():
            if value == "" or value is None:
                return True

        return False

    def update_config_file(self, new_config_dict: dict) -> None:
        with open(self.CONFIG_FILE_PATH, "r", encoding="UTF-8") as config_file:
            try:
                config_dict = json.loads(config_file.read(), encoding="UTF-8")

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: Config.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

        if 'BrowseNodeCrawler' in new_config_dict:
            # BrowseNodeCrawler-Config is updated separately
            # Why separate? Config could concern books OR kindle. A simple update of kindle would delete the values of
            # of books and vice-versa
            node_crawler_config = new_config_dict['BrowseNodeCrawler']
            del new_config_dict['BrowseNodeCrawler']  # Delete ir from dict -> it will be treated separately

            config_dict['BrowseNodeCrawler'].update(node_crawler_config)

            if new_config_dict:  # If there are keys left, update them
                # Should actually be empty (separate updates of each section).
                config_dict.update(new_config_dict)

        else:
            config_dict.update(new_config_dict)

        with open(self.CONFIG_FILE_PATH, "w", encoding="UTF-8") as config_file:
            try:
                config_file.write(json.dumps(config_dict))

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: Config.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

        if self.config_dict["VERBOSE_OUTPUT"]:
            LogHandler.log_message(
                f"{self.HEADER} Successfully updated config.json. New Values: {str(config_dict)}"
            )
        else:
            LogHandler.log_message(f"{self.HEADER} Successfully updated config.json.")

    def update_secrets_file(self, new_secrets_dict: dict) -> None:
        with open(self.SECRETS_FILE_PATH, "r", encoding="UTF-8") as secrets_file:
            try:
                secrets_dict = json.loads(secrets_file.read(), encoding="UTF-8")

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: secrets.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

        secrets_dict.update(new_secrets_dict)

        with open(self.SECRETS_FILE_PATH, "w", encoding="UTF-8") as secrets_file:
            try:
                secrets_file.write(json.dumps(secrets_dict))

            except json.JSONDecodeError:
                raise Exception(
                    f"{self.HEADER} ERROR: secrets.json is not a valid json-File! Please copy the "
                    f"content of the file in the following online-Tool to check the file's syntax "
                    "'https://jsonlint.com/'"
                )

        if self.config_dict["VERBOSE_OUTPUT"]:
            LogHandler.log_message(
                f"{self.HEADER} Successfully updated secrets.json. New Values: {str(new_secrets_dict)}"
            )
        else:
            LogHandler.log_message(f"{self.HEADER} Successfully updated secrets.json.")