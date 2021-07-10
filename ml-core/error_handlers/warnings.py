class WarningJSON(Warning):
    def __init__(self, detail: str):
        self.detail = detail


class BugsNotFoundWarning(WarningJSON):
    detail = "Oops! Bugs haven't been uploaded yet."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)
