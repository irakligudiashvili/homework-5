from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Lecture, Assignment
from api.permissions import IsTeacher, IsEnrolled
from api.serializers import AssignmentSerializer


class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Create a new assignment for a lecture",
        operation_description="""
## Endpoint Description
Allows a teacher enrolled in a course to create a new assignment for a specific lecture.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - lecture: integer, required (ID of the lecture)
    - title: string, required (Assignment title)
    - description: string, optional (Assignment description)

## Responses
- **201 Created**: Assignment successfully created
- **400 Bad Request**: Missing required fields
- **403 Forbidden**: User is not a teacher or not enrolled in the course
- **404 Not Found**: Lecture does not exist
        """,
        request_body=AssignmentSerializer,
        responses={
            201: AssignmentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["assignments"]
    )
    def post(self, request, *args, **kwargs):
        lecture_id = request.data.get('lecture')
        title = request.data.get('title')
        description = request.data.get('description')

        if not lecture_id or not title:
            return Response(
                {'detail': 'Lecture and title are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lecture = get_object_or_404(Lecture, id=lecture_id)

        if not IsEnrolled().user_has_access(request.user, lecture.course):
            return Response(
                {'detail': 'You do not have permission'},
                status=status.HTTP_403_FORBIDDEN
            )

        assignment = Assignment.objects.create(
            lecture=lecture,
            title=title,
            description=description
        )
        serializer = self.get_serializer(assignment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class AssignmentUpdateView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Update an assignment",
        operation_description="""
## Endpoint Description
Allows a teacher to update an existing assignment.

## Path Parameters
- pk: integer, required (Assignment ID)

## Query Parameters
- None

## Request Body
- JSON object containing:
    - title: string, optional
    - description: string, optional

## Responses
- **200 OK**: Assignment successfully updated
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User is not a teacher or not enrolled in the course
- **404 Not Found**: Assignment does not exist
        """,
        request_body=AssignmentSerializer,
        responses={
            200: AssignmentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["assignments"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AssignmentDeleteView(generics.DestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Delete an assignment",
        operation_description="""
## Endpoint Description
Allows a teacher to delete an assignment from a lecture.

## Path Parameters
- pk: integer, required (Assignment ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **204 No Content**: Assignment successfully deleted
- **403 Forbidden**: User is not a teacher or not enrolled in the course
- **404 Not Found**: Assignment does not exist
        """,
        responses={
            204: "Assignment deleted",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["assignments"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AssignmentDetailView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="Retrieve an assignment",
        operation_description="""
## Endpoint Description
Allows an enrolled user to retrieve the details of a specific assignment.

## Path Parameters
- pk: integer, required (Assignment ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns assignment details
- **403 Forbidden**: User is not enrolled in the course
- **404 Not Found**: Assignment does not exist
        """,
        responses={
            200: AssignmentSerializer,
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["assignments"]
    )
    def get_object(self):
        assignment = super().get_object()
        self.check_object_permissions(self.request, assignment.lecture)

        return assignment


class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsEnrolled]

    @swagger_auto_schema(
        operation_summary="List assignments for a lecture",
        operation_description="""
## Endpoint Description
Lists all assignments for a specific lecture. Access is granted to any user enrolled in the course.

## Path Parameters
- lecture_id: integer, required (Lecture ID)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns a list of assignments
- **403 Forbidden**: User is not enrolled in the course
- **404 Not Found**: Lecture does not exist
        """,
        responses={
            200: AssignmentSerializer(many=True),
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["assignments"]
    )
    def get_queryset(self):
        lecture_id = self.kwargs.get('lecture_id')
        lecture = get_object_or_404(Lecture, id=lecture_id)
        self.check_object_permissions(self.request, lecture)
        return Assignment.objects.filter(lecture=lecture)