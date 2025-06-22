from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/<int:pk>/edit/', views.update_student, name='update_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('classrooms/create/', views.create_classroom, name='create_classroom'),
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('classrooms/<int:pk>/edit/', views.update_classroom, name='update_classroom'),
    path('classrooms/<int:pk>/delete/', views.delete_classroom, name='delete_classroom'),
    path('attendance/mark/<int:classroom_id>/', views.mark_attendance, name='mark_attendance'),
    path('students/<int:pk>/classrooms/', views.view_student_classrooms, name='view_student_classrooms'),
    path('students/<int:pk>/attendance/', views.student_attendance_history, name='student_attendance_history'),
    path('attendance/mark/student/<int:student_id>/', views.mark_attendance_for_student, name='mark_attendance_for_student'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    
    path('calendar/<int:student_id>/', views.attendance_calendar, name='attendance_calendar'),
    path('calendar/<int:student_id>/<int:year>/<int:month>/', views.attendance_calendar, name='attendance_calendar_month'),
    path('students/export/pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),

]