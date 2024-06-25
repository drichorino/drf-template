from rest_framework.response import Response

def success_response(data=None, message="Request was successful.", status_code=200):
    response_data = {
        "status": "success",
        "message": message,
        "status_code": status_code,
        "data": data,
    }
    return Response(response_data, status=status_code)

def error_response(message="An error occurred.", error_type="error", status_code=400, data=None):
    if data:
        # Remove sensitive fields
        data.pop('password', None)
        data.pop('confirm_password', None)
    
    # Format message similar to custom_exception_handler
    formatted_message = []
    if isinstance(message, dict):
        for key, value in message.items():
            if isinstance(value, list):
                formatted_message.append(str(value[0]).capitalize())
            elif isinstance(value, dict):
                formatted_message.append({k: str(v).capitalize() for k, v in value.items()})
            else:
                formatted_message.append(str(value).capitalize())
    else:
        formatted_message.append(message)

    # Take only the first error message
    first_error_message = formatted_message[0] if formatted_message else "An error occurred."

    response_data = {
        "status": "failed",
        "message": first_error_message,
        "status_code": status_code,
        "data": data
    }
    return Response(response_data, status=status_code)
