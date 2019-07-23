class LogHandler:
    HEADER = "{0: <20}".format("(LogHandler):")
    output_to_target_method = print
    main_window = None

    @classmethod
    def set_output_target(
        cls,
        standard_stdout: bool = False,
        window: bool = False,
        log_file: bool = False,
        main_window_instance=None,
    ) -> None:
        if standard_stdout:
            cls.output_to_target_method = print
        elif window and main_window_instance is not None:
            cls.main_window = main_window_instance
            cls.output_to_target_method = cls.log_message_to_window
        else:
            cls.output_to_target_method = print

        if log_file:
            raise RuntimeError(f"{cls.HEADER} Writing to log-file not implemented yet!")

    @classmethod
    def log_message_to_window(cls, msg: str) -> None:
        print(msg)
        cls.main_window.Refresh()
        # cls.main_window.ReadNonBlocking()

    @classmethod
    def log_message(cls, msg: str) -> None:
        cls.output_to_target_method(msg)
