class DatabaseEvent:

    @staticmethod
    def add_event(x: int = 0, y: int = 0, range: int = 0, status: str = "", content: str = "",
                  id_game: int = 0) -> int | None:
        pass

    @staticmethod
    def get_event(id_event) -> dict | None:
        pass
    
    @staticmethod
    def get_all_events() -> list | None:
        pass
