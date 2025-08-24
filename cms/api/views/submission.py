from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.permissions import IsStudent, IsEnrolled, IsOwner, IsTeacher
from api.serializers import SubmissionSerializer
from api.models import Submission, Enrollment


class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Create a submission",
        operation_description="""
## Endpoint Description
Allows a student to submit work for an assignment.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - assignment: integer, required (assignment ID)
    - content: string, required (submission content)

## Responses
- **201 Created**: Submission successfully created
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User not enrolled in the course of the assignment
        """,
        request_body=SubmissionSerializer,
        responses={
            201: openapi.Response(
                description="Submission created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "assignment": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "content": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    example={
                        "id": 1,
                        "assignment": 3,
                        "user": 5,
                        "content": "My submission content",
                    }
                )
            ),
            400: "Validation error",
            403: "User not enrolled in course"
        },
        tags=["submissions"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = serializer.validated_data['assignment']
        course = assignment.lecture.course

        if not IsEnrolled.user_has_access(request.user, course):
            raise PermissionDenied(
                'You are not enrolled in the course of this assignment'
            )

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmissionRetrieveView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwner | (IsTeacher & IsEnrolled)]

    @swagger_auto_schema(
        operation_summary="Retrieve a submission",
        operation_description="""
## Endpoint Description
Retrieve a specific submission by its ID.

## Path Parameters
- pk: integer, required (submission ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns submission details
- **404 Not Found**: Submission does not exist
- **403 Forbidden**: Access denied
        """,
        responses={
            200: SubmissionSerializer,
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["submissions"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsOwner | (IsTeacher & IsEnrolled)]

    @swagger_auto_schema(
        operation_summary="List submissions",
        operation_description="""
## Endpoint Description
Lists submissions visible to the current user.

- Students see only their own submissions.
- Teachers see submissions for courses they are enrolled in.
        """,
        responses={200: SubmissionSerializer(many=True)},
        tags=["submissions"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return Submission.objects.filter(user=user)
        elif user.role == 'teacher':
            courses = Enrollment.objects.filter(user=user).values_list(
                'course', flat=True
            )
            return Submission.objects.filter(
                assignment__lecture__course__in=courses
            )

        return Submission.objects.all()
