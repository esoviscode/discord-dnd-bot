class DatabaseDialog:

    @staticmethod
    def add_dialog(id_speaker: int = 0, id_listener: int = 0, content: str = "", status: str = "") -> int | None:
        pass

    @staticmethod
    def update_dialog(id_dialog: int, status: str = "") -> None:
        pass

    @staticmethod
    def get_dialog(id_dialog: int = 0) -> dict | None:
        pass

    @staticmethod
    def get_all_dialogs() -> list | None:
        pass
