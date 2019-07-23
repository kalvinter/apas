from collections import deque

import sys
import pathlib
import os


class StartUpHandler:
    HEADER = "{0: <20}".format("(StartUpHandler):")
    REQUIRED_FOLDERS = ['data', 'csv_output', 'config']
    ROOT_DIR = None
    MESSAGE_QUEUE = deque()

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        self.IN_STARTUP_PHASE = True

        self.load_start_up_variables()

        self.check_create_necessary_folder_exist()

    def load_start_up_variables(self):
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            print(f"{self.HEADER} Running in a bundled exe!")
            self.ROOT_DIR = pathlib.Path(sys.executable).resolve().parent
        else:
            # we are running in a normal Python environment
            self.ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

        msg = f"{self.HEADER} [OK] Successfully loaded start-up-variables."
        self.log_start_up_message(msg=msg)

    def check_create_necessary_folder_exist(self) -> None:
        for folder in self.REQUIRED_FOLDERS:
            folder_path = str(pathlib.Path.joinpath(self.ROOT_DIR, folder))
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
                msg = f"{self.HEADER} [WARNING] Created missing folder: {folder_path}."
                self.log_start_up_message(msg=msg)

            else:
                print(f"{self.HEADER} [INFO] Found folder {folder_path}.")

        msg = f"{self.HEADER} [OK] All necessary folders exist."
        self.log_start_up_message(msg=msg)

    def in_start_up_phase(self):
        return self.IN_STARTUP_PHASE

    def end_startup_phase(self):
        self.IN_STARTUP_PHASE = False

    def log_start_up_message(self, msg: str):
        print(msg)
        self.MESSAGE_QUEUE.append(msg)

    def print_start_up_messages(self) -> None:
        while len(self.MESSAGE_QUEUE) > 0:
            print(self.MESSAGE_QUEUE.popleft())
