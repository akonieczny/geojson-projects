import abc


class BaseError(Exception, abc.ABC):
    pass


class NotFoundError(BaseError):
    pass


class AlreadyExistError(BaseError):
    pass
