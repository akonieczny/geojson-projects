class BaseError(Exception):
    message_template: str = "{}"

    def __init__(self, *args: str, **kwargs: str) -> None:
        self.message = self.message_template.format(*args, **kwargs)
        super().__init__(self.message)


class NotFoundError(BaseError):
    message_template = "Not found"


class AlreadyExistError(BaseError):
    message_template = "Object with at least one passed fields (which is required as unique) already exist"
