from pydantic import ValidationError, BaseModel
from pydantic.error_wrappers import ErrorWrapper


def validation_error(name: str, msg: str):
    return ValidationError([ErrorWrapper(Exception(msg), name)], BaseModel)
