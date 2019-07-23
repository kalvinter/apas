from apas.util.logging import LogHandler
from amazon.api import AmazonAPI

from urllib.error import HTTPError
import time


class APIHandler:
    HEADER = "{0: <20}".format("(APIHandler):")

    AMAZON_NAMESPACE = {
        "owl": "http://webservices.amazon.com/AWSECommerceService/2013-08-01"
    }
    RETRY_LIMIT = 5
    COOLDOWN_TIME_FOR_RETRY = 10
    AMAZON_API = None

    AMAZON_ACCESS_KEY = None
    AMAZON_SECRET_KEY = None
    AMAZON_ASSOC_TAG = None
    RETRY_ERROR_MESSAGE = f"{HEADER} ERROR: Could not reach API!"

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def create_api_connection(self, config_dict: dict, secrets_dict: dict):
        try:
            self.AMAZON_ACCESS_KEY = secrets_dict["AMAZON_ACCESS_KEY"]
            self.AMAZON_SECRET_KEY = secrets_dict["AMAZON_SECRET_KEY"]
            self.AMAZON_ASSOC_TAG = secrets_dict["AMAZON_ASSOC_TAG"]

        except Exception as e:
            raise Exception(
                f"{self.HEADER} FATAL: Could not read necessary access-, secret-key and association "
                f"tag from config. Error-Msg: {str(e)}"
            )

        try:
            self.RETRY_LIMIT = int(config_dict["RETRY_LIMIT"])
            self.COOLDOWN_TIME_FOR_RETRY = int(config_dict["COOLDOWN_TIME_FOR_RETRY"])

        except Exception as e:
            LogHandler.log_message(
                f"{self.HEADER} WARNING: Could not read API-Handler-Values from config. Using default "
                f"values instead. Error-Msg: {str(e)}"
            )

        self.RETRY_ERROR_MESSAGE = (
            f"{self.HEADER} ERROR: Could not reach API after {self.RETRY_LIMIT} retries!"
        )

        try:
            self.AMAZON_API = AmazonAPI(
                self.AMAZON_ACCESS_KEY,
                self.AMAZON_SECRET_KEY,
                self.AMAZON_ASSOC_TAG,
                region="DE",
                MaxQPS=0.5,
            )

        except TypeError as e:
            LogHandler.log_message(
                f"{self.HEADER} ERROR: Could not initialize Amazon-API-Connection! Have you "
                f"provided correct values in your secrets.json-File? Msg.: {str(e)}"
            )

    def api_call_with_retry(self, function, function_params: dict) -> list:
        time.sleep(1)
        result = None
        counter = 1
        while counter <= self.RETRY_LIMIT and not result:

            try:
                result = function(**function_params)

            except HTTPError:
                LogHandler.log_message(
                    f"{self.HEADER} WARNING (Nr. {counter}): API Call failed. Retrying "
                    f"in {self.COOLDOWN_TIME_FOR_RETRY} seconds ..."
                )
                counter += 1
                time.sleep(self.COOLDOWN_TIME_FOR_RETRY)

        if not result:
            raise Exception(self.RETRY_ERROR_MESSAGE)

        return result

    def browse_node_lookup(self, **kwargs):
        return self.AMAZON_API.browse_node_lookup(**kwargs)

    def lookup(self, **kwargs):
        return self.AMAZON_API.lookup(**kwargs)
