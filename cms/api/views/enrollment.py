from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.permissions import IsTeacher, IsEnrolled
from api.serializers import EnrollmentSerializer
from api.models import Course, User, Enrollment


class EnrollInCourseView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Enroll a user in a course",
        operation_description="""
## Endpoint Description
Allows a teacher to enroll a specific user (student or another teacher) into a course.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - course_id: integer, required (ID of the course to enroll in)
    - user_id: integer, required (ID of the user to enroll)

## Responses
- **201 Created**: User successfully enrolled
- **400 Bad Request**: Missing required fields or user is already enrolled
- **403 Forbidden**: User is not a teacher or not enrolled in the course they are trying to manage
- **404 Not Found**: Course or user does not exist
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['course_id', 'user_id'],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            example={
                'course_id': 1,
                'user_id': 5,
            }
        ),
        responses={
            201: EnrollmentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["courses"]
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')

        if not course_id or not user_id:
            return Response(
                {'detail': 'course_id and user_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response(
                {'detail': 'User is already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment = Enrollment.objects.create(user=user, course=course)
        serializer = self.get_serializer(enrollment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnenrollFromCourseView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacher, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Unenroll a user from a course",
        operation_description="""
## Endpoint Description
Allows a teacher to unenroll a user from a course.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - course_id: integer, required (ID of the course to unenroll from)
    - user_id: integer, required (ID of the user to unenroll)

## Responses
- **200 OK**: User successfully unenrolled
- **400 Bad Request**: Missing required fields or course owner cannot be unenrolled
- **403 Forbidden**: User is not a teacher or not enrolled in the course they are trying to manage
- **404 Not Found**: Course or enrollment does not exist
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['course_id', 'user_id'],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            example={
                'course_id': 1,
                'user_id': 5,
            }
        ),
        responses={
            200: "User unenrolled",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["courses"]
    )
    def delete(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')

        if not course_id or not user_id:
            return Response(
                {'detail': 'course_id and user_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            enrollment = Enrollment.objects.get(user_id=user_id, course=course)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'User is not enrolled in this course'},
                status=status.HTTP_404_NOT_FOUND
            )

        if enrollment.user == course.owner:
            return Response(
                {'detail': 'Course owner cannot be unenrolled'},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment.delete()

        return Response(
            {'detail': 'User unenrolled'},
            status=status.HTTP_200_OK
        )
