from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="""
## Endpoint Description
Creates a new user in the system.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - first_name: string, required
    - last_name: string, required
    - email: string, required
    - password: string, required
    - role: string, optional

## Responses
- **201 Created**: User successfully created
- **400 Bad Request**: Validation errors in the request body
        """,
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING)
                    },
                    example={"message": "User created successfully"}
                )
            ),
            400: openapi.Response(
                description="Validation error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"first_name": ["This field is required."]}
                )
            )
        },
        tags=["users"]
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
