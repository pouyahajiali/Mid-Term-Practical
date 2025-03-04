from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('register/', views.student_register, name='register'),
    path('add-textbook/', views.add_textbook_page, name='add_textbook'),
    path('my-textbooks/', views.my_textbooks_page, name='my_textbooks'),
    path('textbooks/<str:course_code>/', views.textbook_list_by_course_page, name='textbook_list_by_course'),
    path('delete-textbook/<int:textbook_id>/', views.delete_textbook_page, name='delete_textbook'),
    path('', views.home_page, name='home'),
    path('logout/', views.logout_page, name='logout'),
]
