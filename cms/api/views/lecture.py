from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Course, Enrollment, Lecture
from api.permissions import IsTeacher, IsEnrolled
from api.serializers import LectureSerializer


class LectureCreateView(generics.CreateAPIView):
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Create a new lecture",
        operation_description="""
## Endpoint Description
Allows a teacher to create a new lecture within a course.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - course: integer, required (course ID)
    - topic: string, required (lecture topic)
    - file: file, required (lecture file)

## Responses
- **201 Created**: Lecture successfully created
- **400 Bad Request**: Missing required fields
- **403 Forbidden**: User not enrolled in the course as a teacher
- **404 Not Found**: Course does not exist
        """,
        request_body=LectureSerializer,
        responses={
            201: openapi.Response(
                description="Lecture created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "course": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "topic": openapi.Schema(type=openapi.TYPE_STRING),
                        "file": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    example={
                        "id": 1,
                        "course": 1,
                        "topic": "Introduction to DRF",
                        "file": "http://example.com/media/lectures/lecture1.pdf"
                    }
                )
            ),
            400: "Missing required fields",
            403: "User not enrolled as a teacher",
            404: "Course not found"
        },
        tags=["lectures"]
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        topic = request.data.get('topic')
        file = request.data.get('file')

        if not course_id or not topic or not file:
            return Response(
                {'detail': 'course, topic and file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists():
            return Response(
                {'detail': 'Enroll in this course to create lectures'},
                status=status.HTTP_403_FORBIDDEN
            )

        lecture = Lecture.objects.create(
            course=course,
            topic=topic,
            file=file
        )
        serializer = self.get_serializer(lecture)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LectureDetailView(generics.RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Retrieve a lecture",
        operation_description="""
## Endpoint Description
Allows an enrolled user to retrieve the details of a specific lecture.

## Path Parameters
- pk: integer, required (lecture ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns lecture details
- **403 Forbidden**: User not enrolled in the course
- **404 Not Found**: Lecture does not exist
        """,
        responses={
            200: LectureSerializer,
            403: "User not enrolled in the course",
            404: "Not Found"
        },
        tags=["lectures"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LectureListView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="List lectures for a course",
        operation_description="""
## Endpoint Description
Lists all lectures for a specific course.

## Path Parameters
- course_id: integer, required (course ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns a list of lectures
- **403 Forbidden**: User not enrolled in the course
- **404 Not Found**: Course does not exist
        """,
        responses={
            200: LectureSerializer(many=True),
            403: "User not enrolled in the course",
            404: "Course not found"
        },
        tags=["lectures"]
    )
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)

        if course.owner != self.request.user and not Enrollment.objects.filter(
            user=self.request.user,
            course=course
        ).exists():
            raise PermissionDenied('You are not enrolled in this course')

        return Lecture.objects.filter(course=course)


class LectureAllListView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all lectures",
        operation_description="""
## Endpoint Description
Lists all lectures across all courses that the authenticated user has access to.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns a list of lectures
        """,
        responses={
            200: LectureSerializer(many=True),
        },
        tags=["lectures"]
    )
    def get_queryset(self):
        user = self.request.user
        all_lectures = Lecture.objects.all()
        accessible_lectures = []

        for lecture in all_lectures:
            if IsEnrolled().user_has_access(user, lecture.course):
                accessible_lectures.append(lecture)

        return accessible_lectures


class LectureUpdateView(generics.UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Update a lecture",
        operation_description="""
## Endpoint Description
Allows the teacher who owns the course to update a specific lecture.

## Path Parameters
- pk: integer, required (lecture ID)

## Query Parameters
- None

## Request Body
- JSON object containing:
    - topic: string, optional
    - file: file, optional

## Responses
- **200 OK**: Lecture successfully updated
- **403 Forbidden**: User is not the owner of the course
- **404 Not Found**: Lecture does not exist
        """,
        request_body=LectureSerializer,
        responses={
            200: LectureSerializer,
            403: "User is not the course owner",
            404: "Not Found"
        },
        tags=["lectures"]
    )
    def get_object(self):
        lecture = super().get_object()

        return lecture


class LectureDeleteView(generics.DestroyAPIView):
    queryset = Lecture.objects.all()
    permission_classes = [IsAuthenticated, IsTeacher]

    @swagger_auto_schema(
        operation_summary="Delete a lecture",
        operation_description="""
## Endpoint Description
Allows a teacher to delete a lecture from a course they are associated with.

## Path Parameters
- pk: integer, required (lecture ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **204 No Content**: Lecture successfully deleted
- **403 Forbidden**: User not associated with the course
- **404 Not Found**: Lecture does not exist
        """,
        responses={
            204: "Lecture deleted",
            403: "User is not associated with the course",
            404: "Not Found"
        },
        tags=["lectures"]
    )
    def get_object(self):
        lecture = super().get_object()

        return lecture
