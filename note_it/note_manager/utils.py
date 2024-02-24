from rest_framework.response import Response
from rest_framework import status




def success_response(data=None, message="Success", status_code=200):
    return Response({
        "data": data,
        "success": True,
        "message": message
    }, status=status_code)

def error_response(errors=None, message="Error", status_code=400):
    return Response({
        "errors": errors,
        "success": False,
        "message": message
    }, status=status_code)