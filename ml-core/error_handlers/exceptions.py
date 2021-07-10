class ExceptionJSON(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class SmallNumberRepresentatives(ExceptionJSON):
    detail = "Oops! Too small number of class representatives."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class LittleDataToAnalyze(ExceptionJSON):
    detail = "Oops! Too little data to analyze. Model can't be trained."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class ResolutionElementsMissed(ExceptionJSON):
    detail = "Oops! Resolution elements are missed. Model can't be trained."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class IncorrectPredictionsTableOrder(ExceptionJSON):
    detail = "Incorrect predictions table positions order"

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class NotFilledDefaultFields(ExceptionJSON):
    detail = "Not all mandatory default fields are specified"

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class InvalidSourceField(ExceptionJSON):
    detail = "Source field isn't presented in your data"

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class InconsistentGivenData(ExceptionJSON):
    detail = "Cannot train models. Given data is inconsistent."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class BugResolutionEmpty(ExceptionJSON):
    detail = "Bug resolutions are empty. Model can't be trained."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)


class AreaOfTestingEmpty(ExceptionJSON):
    detail = "Areas of Testing are empty. Model can't be trained."

    def __init__(self, detail=detail) -> None:
        super().__init__(detail=detail)
