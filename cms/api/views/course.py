from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Enrollment, Course
from api.permissions import IsOwner, IsTeacher, IsEnrolled
from api.serializers import CourseSerializer, CourseDetailSerializer


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Create a new course",
        operation_description="""
## Endpoint Description
Allows an authenticated user with a 'teacher' role to create a new course. The teacher is automatically enrolled in the new course upon creation.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - title: string, required (Course title)
    - description: string, optional (Course description)

## Responses
- **201 Created**: Course successfully created
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User is not a teacher
        """,
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: "Bad Request",
            403: "Forbidden"
        },
        tags=["courses"]
    )
    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        Enrollment.objects.get_or_create(user=self.request.user, course=course)


class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsTeacher, IsOwner]

    @swagger_auto_schema(
        operation_summary="Delete a course",
        operation_description="""
## Endpoint Description
Allows the owner of a course to delete it.

## Path Parameters
- pk: integer, required (Course ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **204 No Content**: Course successfully deleted
- **403 Forbidden**: User is not the course owner or not a teacher
- **404 Not Found**: Course does not exist
        """,
        responses={
            204: "Course deleted",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["courses"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsOwner]

    @swagger_auto_schema(
        operation_summary="Update a course",
        operation_description="""
## Endpoint Description
Allows the owner of a course to update its details.

## Path Parameters
- pk: integer, required (Course ID)

## Query Parameters
- None

## Request Body
- JSON object containing:
    - title: string, optional
    - description: string, optional

## Responses
- **200 OK**: Course successfully updated
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User is not the course owner or not a teacher
- **404 Not Found**: Course does not exist
        """,
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["courses"]
    )
    def update(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Retrieve a course",
        operation_description="""
## Endpoint Description
Allows an enrolled user to retrieve the details of a specific course.

## Path Parameters
- pk: integer, required (Course ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns course details
- **403 Forbidden**: User is not enrolled in the course
- **404 Not Found**: Course does not exist
        """,
        responses={
            200: CourseDetailSerializer,
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["courses"]
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseListView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all accessible courses",
        operation_description="""
## Endpoint Description
Lists all courses that the authenticated user has access to, based on their enrollment status.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns a list of accessible courses
        """,
        responses={
            200: CourseDetailSerializer(many=True),
        },
        tags=["courses"]
    )
    def get_queryset(self):
        user = self.request.user
        all_courses = Course.objects.all()
        accessible_courses = []

        for course in all_courses:
            if IsEnrolled.user_has_access(user, course):
                accessible_courses.append(course)

        return accessible_courses
