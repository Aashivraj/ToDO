"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ToDoList.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LoginFormView.as_view(),name="login"),
   
    path('home/',home.as_view(),name="home"),
    path('add_todo/',add_todo.as_view(),name="add_todo"),
    path('add_user/',AddUserView.as_view(),name="add_user"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('update_comment/<int:id>', UpdateTodoComment.as_view(), name="updatecomment"),
    # path('update_teamtodo_comment/<int:id>', UpdateTeamTodoComment.as_view(), name="updateteamtodocomment"),
    path('todo/<int:todo_id>/notes/', NoteHistoryView.as_view(), name='note_history'),
 
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    
    path('notifications/mark_all_as_read/', mark_all_as_read, name='mark_all_as_read'),
    path('mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/clear_all/', clear_all_notifications, name='clear_all_notifications'),
    path('update_user/<int:id>', UpdateUserView.as_view(), name="update"),
    path('delete/<int:id>',DeleteUserView.as_view(),name='delete'),
    path('user_list/',UserListView.as_view(),name="userlist"),
    path('todo_list/',ToDoListView.as_view(),name="todolist"),
    path('update_todo_status/<int:todo_id>/',update_todo.as_view(), name='update_todo_status'),
    path('update_todo_start_time/<int:todo_id>/', UpdateTodoStartTime.as_view(), name='update_todo_start_time'),
   
    
    path('Profile/',ProfilePageView.as_view(),name="profile"),

    
    #team Lead Dashboard
    path('teamtodo/',TeamLeadView.as_view(),name="teamtodo"),
    path('system_settings/',SettingsView.as_view(),name="system_settings"),
    
    path('user/<int:user_id>/task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),

    path('error/',ErrorView.as_view(),name="error"),
    path('users/toggle/<int:user_id>/', ToggleActiveStatusView.as_view(), name='toggle_active_status'),
    path('team/',TeamView.as_view(),name="team"),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='admin_templates/change_password.html',success_url='/'),name='change_password'),
    
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)