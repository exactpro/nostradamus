class ConfigExceptions(Exception):
    pass


class IncorrectValueError(ConfigExceptions):
    pass


class NotExist(Exception):
    pass


class NotExistFile(NotExist):
    pass


class NotExistModel(NotExist):
    pass


class NotExistField(NotExist):
    pass


class LDAPError(Exception):
    pass


class ModelNotFound(Exception):
    pass


class ModelsNotFound(Exception):
    pass


class InconsistentDataError(Exception):
    pass