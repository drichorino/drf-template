from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_details = []

        for key, value in response.data.items():
            # Check if the value is a list or dictionary and format accordingly
            if isinstance(value, list):
                formatted_value = [str(v).capitalize() for v in value]
            elif isinstance(value, dict):
                formatted_value = {k: str(v).capitalize() for k, v in value.items()}
            else:
                formatted_value = str(value).capitalize()

            error_details.append({"field": key, "message": formatted_value})

        # Convert the QueryDict to a regular dictionary and exclude csrfmiddlewaretoken
        if "request" in context:
            request_data = (
                context["request"].data.dict()
                if hasattr(context["request"].data, "dict")
                else context["request"].data
            )
        else:
            request_data = {}

        request_data.pop("csrfmiddlewaretoken", None)

        # Take only the first error message
        first_error_message = error_details[0]["message"] if error_details else "An error occurred."

        custom_response_data = {
            "status": "failed",
            "message": first_error_message,
            "status_code": response.status_code,
            "data": request_data,
        }
        response.data = custom_response_data

    return response
