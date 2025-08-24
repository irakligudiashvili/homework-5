from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.models import Submission, Comment
from api.permissions import IsOwner, IsTeacher, IsEnrolled
from api.serializers.comment import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner | (IsTeacher & IsEnrolled)]

    @swagger_auto_schema(
        operation_summary="Create a new comment on a submission",
        operation_description="""
## Endpoint Description
Allows a student (owner of the submission) or a teacher (enrolled in the course) to add a comment to a specific submission.

## Path Parameters
- None

## Query Parameters
- None

## Request Body
- JSON object containing:
    - submission: integer, required (ID of the submission to comment on)
    - content: string, required (The comment content)

## Responses
- **201 Created**: Comment successfully created
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User does not have permission to comment on the submission
- **404 Not Found**: Submission does not exist
        """,
        request_body=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["comments"]
    )
    def perform_create(self, serializer):
        submission_id = self.request.data.get('submission')
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response(
                {'detail': 'Submission not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # The check_object_permissions call handles the IsOwner | (IsTeacher & IsEnrolled) logic
        self.check_object_permissions(self.request, submission)

        serializer.save(user=self.request.user, submission=submission)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner | (IsTeacher & IsEnrolled)]

    @swagger_auto_schema(
        operation_summary="List comments for a submission",
        operation_description="""
## Endpoint Description
Lists all comments for a specific submission. Access is granted to the owner of the submission (student) or a teacher enrolled in the course.

## Path Parameters
- submission_id: integer, required (ID of the submission)

## Query Parameters
- None

## Request Body
- None

## Responses
- **200 OK**: Returns a list of comments
- **403 Forbidden**: User does not have permission to view comments for this submission
- **404 Not Found**: Submission does not exist
        """,
        responses={
            200: CommentSerializer(many=True),
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["comments"]
    )
    def get_queryset(self):
        submission_id = self.kwargs.get('submission_id')
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response(
                {'detail': 'Submission not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # The check_object_permissions call handles the IsOwner | (IsTeacher & IsEnrolled) logic
        self.check_object_permissions(self.request, submission)

        return Comment.objects.filter(submission=submission)


class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_summary="Update a comment",
        operation_description="""
## Endpoint Description
Allows the owner of a comment to update its content.

## Path Parameters
- pk: integer, required (ID of the comment)

## Query Parameters
- None

## Request Body
- JSON object containing:
    - content: string, optional (The updated comment content)

## Responses
- **200 OK**: Comment successfully updated
- **400 Bad Request**: Validation errors
- **403 Forbidden**: User is not the owner of the comment
- **404 Not Found**: Comment does not exist
        """,
        request_body=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["comments"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_summary="Delete a comment",
        operation_description="""
## Endpoint Description
Allows the owner of a comment to delete it.

## Path Parameters
- pk: integer, required (ID of the comment)

## Query Parameters
- None

## Request Body
- None

## Responses
- **204 No Content**: Comment successfully deleted
- **403 Forbidden**: User is not the owner of the comment
- **404 Not Found**: Comment does not exist
        """,
        responses={
            204: "Comment deleted",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["comments"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
