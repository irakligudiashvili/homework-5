from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.permissions import IsTeacher, IsEnrolled, IsOwner
from api.serializers import GradeSerializer
from api.models import Grade


class GradeCreateView(generics.CreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Create a new grade for a submission",
        operation_description="""
## Endpoint Description
Allows a teacher to grade a specific submission.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - submission: integer, required (submission ID)
    - score: integer, required (grade score)
    - comments: string, optional (grade comments)

## Responses
- **201 Created**: Grade successfully created
- **400 Bad Request**: Validation errors (e.g., missing fields)
- **403 Forbidden**: User is not a teacher or not enrolled in the course
        """,
        request_body=GradeSerializer,
        responses={
            201: openapi.Response(
                description="Grade created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "submission": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "teacher": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "score": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "comments": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    example={
                        "id": 1,
                        "submission": 5,
                        "teacher": 3,
                        "score": 95,
                        "comments": "Great work!"
                    }
                )
            ),
            400: "Bad Request",
            403: "Forbidden"
        },
        tags=["grades"]
    )
    def perform_create(self, serializer):
        submission = serializer.validated_data['submission']
        course = submission.assignment.lecture.course

        if not IsEnrolled.user_has_access(self.request.user, course):
            raise PermissionDenied(
                'You must be enrolled in the course to grade'
            )

        serializer.save(teacher=self.request.user)


class GradeRetrieveView(generics.RetrieveAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsOwner | (IsTeacher & IsEnrolled)]

    @swagger_auto_schema(
        operation_summary="Retrieve a grade",
        operation_description="""
## Endpoint Description
Allows a student to view their own grade or a teacher to view a grade for a course they are enrolled in.

## Path Parameters
- pk: integer, required (grade ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns grade details
- **403 Forbidden**: Access denied
- **404 Not Found**: Grade does not exist
        """,
        responses={
            200: GradeSerializer,
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["grades"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GradeUpdateView(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Update a grade",
        operation_description="""
## Endpoint Description
Allows a teacher to update an existing grade for a submission within a course they are enrolled in.

## Path Parameters
- pk: integer, required (grade ID)

## Query Parameters
- None

## Request Body
- JSON object containing:
    - score: integer, optional
    - comments: string, optional

## Responses
- **200 OK**: Grade successfully updated
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User not enrolled in the course as a teacher
- **404 Not Found**: Grade does not exist
        """,
        request_body=GradeSerializer,
        responses={
            200: GradeSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["grades"]
    )
    def perform_update(self, serializer):
        submission = serializer.instance.submission
        course = submission.assignment.lecture.course

        if not IsEnrolled.user_has_access(self.request.user, course):
            raise PermissionDenied(
                'You must be enrolled in the course to update this grade'
            )

        serializer.save(teacher=self.request.user)


class GradeDeleteView(generics.DestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Delete a grade",
        operation_description="""
## Endpoint Description
Allows a teacher to delete a grade from a submission within a course they are enrolled in.

## Path Parameters
- pk: integer, required (grade ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **204 No Content**: Grade successfully deleted
- **403 Forbidden**: User not enrolled in the course as a teacher
- **404 Not Found**: Grade does not exist
        """,
        responses={
            204: "Grade deleted",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["grades"]
    )
    def perform_destroy(self, instance):
        course = instance.submission.assignment.lecture.course

        if not IsEnrolled.user_has_access(self.request.user, course):
            raise PermissionDenied(
                'You must be enrolled in the course to delete this grade'
            )

        instance.delete()
