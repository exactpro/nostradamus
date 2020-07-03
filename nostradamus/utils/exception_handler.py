from rest_framework.views import exception_handler as old_exception_handler
from rest_framework.response import Response

from utils.const import DEFAULT_ERROR_CODE, DEFAULT_WARNING_CODE


def exception_handler(exc: Exception, context: dict) -> Response:
    """ Creates response that will be returned for any exception.

    Parameters:
    ----------
    exc:
        Raised exception.
    context:
        Response context.

    Returns:
    ----------
        Http response with parsed data.
    """
    response = old_exception_handler(exc, context)

    if response:
        if hasattr(response.data, "serializer"):
            parse_validation_errors(response)
        response.data["message"] = getattr(exc, "message", "")

        if isinstance(exc, Warning):
            response.data = {"warning": response.data}
        else:
            response.data = {"exception": response.data}

    return response


def parse_validation_errors(response: Response):
    """ Makes response data more readable.

    Parameters:
    ----------
    response:
        Http response which contains descriptions for all validation errors
        for model fields.

    """
    error_list = [
        {"name": key, "errors": response.data[key]} for key in response.data
    ]

    response.data = {"fields": error_list}
