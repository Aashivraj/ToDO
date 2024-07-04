from django.urls import path
from ToDoList.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    
    #Authentication-URLS
    path('',LoginView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('error/',ErrorView.as_view(),name="error"),
    path('change_password/',ChangePasswordView.as_view(),name='change_password'),
    
    
    #Main-URLS
    path('home/',Dashboard.as_view(),name="home"),
    path('Profile/',ProfilePageView.as_view(),name="profile"),
    
    
    #User-URLS
    path('add_user/',UserView_Add.as_view(),name="add_user"),
    path('update_user/<int:id>', UserView_Update.as_view(), name="update"),
    path('user_list/',UserView_List.as_view(),name="userlist"),
    path('delete/<int:id>',UserView_Delete.as_view(),name='delete'),
    
    
    #Todos-URLS
    path('add_todo/',TodoView_Add.as_view(),name="add_todo"),
    path('todo_list/',TodoView_List.as_view(),name="todolist"),
    path('update_comment/<int:id>', TodoComment.as_view(), name="updatecomment"),
    
    
    #Todos-Others-URLS
    path('todo/<int:todo_id>/notes/', NoteHistoryView.as_view(), name='note_history'),
    path('update_todo_status/<int:todo_id>/',TodoView_Update.as_view(), name='update_todo_status'),
    path('update_todo_start_time/<int:todo_id>/', TodoView_StartTime.as_view(), name='update_todo_start_time'),
    
    
    #Notifications-URLS
    path('notifications/', NotificationListView.as_view(), name='notifications'),
   
   
    #Notifications-URLS-FunctionBased
    path('notifications/mark_all_as_read/', mark_all_as_read, name='mark_all_as_read'),
    path('mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/clear_all/', clear_all_notifications, name='clear_all_notifications'),
   
    
    #Team-URLS
    path('teamtodo/',TeamTodoView.as_view(),name="teamtodo"),
    path('team/',TeamView.as_view(),name="team"),
    
    
    #Others-URLS
    path('system_settings/',SettingsView.as_view(),name="system_settings"),
    path('user/<int:user_id>/task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('users/toggle/<int:user_id>/', ToggleActiveStatusView.as_view(), name='toggle_active_status'),
    
 
]

