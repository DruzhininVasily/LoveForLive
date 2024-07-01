from django.urls import path
from . import views

urlpatterns = [
    path('', views.CoursesView.as_view(), name='courses'),
    path('course-info/<int:pk>', views.InfoView.as_view(), name='course_info'),
    path('<slug>', views.CourseDetailPage.as_view(), name='course'),
    path('dossing/<slug>', views.DossingView.as_view(), name='dossing'),
    path('<slug>/<lesson_slug>', views.LessonDetailPage.as_view(), name='lesson'),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
]
