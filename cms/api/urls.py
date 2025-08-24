from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from api.views.assignment import AssignmentCreateView, AssignmentDetailView, \
    AssignmentUpdateView, AssignmentDeleteView, AssignmentListView
from api.views.comment import CommentListView, CommentCreateView, \
    CommentUpdateView, CommentDeleteView
from api.views.course import CourseListView, CourseCreateView, \
    CourseDetailView, CourseUpdateView, CourseDeleteView
from api.views.enrollment import EnrollInCourseView, UnenrollFromCourseView
from api.views.grade import GradeDeleteView, GradeUpdateView, \
    GradeRetrieveView, GradeCreateView
from api.views.lecture import LectureListView, LectureCreateView, \
    LectureDetailView, LectureUpdateView, LectureDeleteView, LectureAllListView
from api.views.submission import SubmissionCreateView, SubmissionRetrieveView, \
    SubmissionListView
from api.views.user import UserRegistrationView

urlpatterns = [
    # Auth
    path('auth/register/', UserRegistrationView.as_view(),name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Courses
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),

    # Enrollment
    path('courses/enroll/', EnrollInCourseView.as_view(), name='course-enroll'),
    path('courses/unenroll/', UnenrollFromCourseView.as_view(), name='course-unenroll'),

    # Lectures
    path('lectures/', LectureAllListView.as_view(), name='lecture-list-all'),
    path('lectures/create/', LectureCreateView.as_view(), name='lecture-create'),
    path('lectures/<int:pk>/', LectureDetailView.as_view(), name='lecture-detail'),
    path('lectures/course/<int:course_id>/', LectureListView.as_view(), name='lecture-list'),
    path('lectures/<int:pk>/update/', LectureUpdateView.as_view(), name='lecture-update'),
    path('lectures/<int:pk>/delete/', LectureDeleteView.as_view(), name='lecture-delete'),

    # Assignments
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment-update'),
    path('assignments/<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment-delete'),
    path('assignments/lecture/<int:lecture_id>/', AssignmentListView.as_view(), name='assignment-list'),

    # Submissions
    path('submissions/create/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionRetrieveView.as_view(), name='submission-detail'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),

    # Grades
    path('grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/', GradeRetrieveView.as_view(), name='grade-retrieve'),
    path('grades/<int:pk>/update/', GradeUpdateView.as_view(), name='grade-update'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade-delete'),

    # Comments
    path('submissions/<int:submission_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
