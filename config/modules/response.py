from config.modules.exceptions import CustomError, Error
from functools import wraps


def success(data: object) -> dict:

    res = {
        "code": 0,
        "msg": "SUCCESS",
        "data": data
    }
    return res


def custom_error(e: CustomError) -> dict:
    res = {
        "code": e.code,
        "error": e.error,
        "msg": e.error_msg
    }
    return res


def exception(e: Exception) -> dict:
    res = {
        "code": Error.ERROR.value,
        "error": type(e).__name__,
        "msg": str(e)
    }
    return res


def send_format(func):
    """
    Response 기본 형태
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return success(result)
        except CustomError as e:
            return custom_error(e)
        except Exception as e:
            return exception(e)
    return wrapper
