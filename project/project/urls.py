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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginFormView.as_view(),name="login"),
   
    path('home/',home.as_view(),name="home"),
    path('add_todo/',add_todo.as_view(),name="add_todo"),
    path('add_user/',AddUserView.as_view(),name="add_user"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('update_user/<int:id>', UpdateUserForm.as_view(), name="update"),
    path('delete/<int:id>',DeleteUserView.as_view(),name='delete'),
    path('user_list/',UserListView.as_view(),name="userlist"),
    path('todo_list/',ToDoListView.as_view(),name="todolist"),
    path('update_todo_status/<int:todo_id>/',update_todo.as_view(), name='update_todo_status'),
    path('admintodolist/',AdminHomeToDoView.as_view(),name="admintodolist"),
    
    #team Lead Dashboard
    path('teamtodo/',teamlead.as_view(),name="teamtodo"),

    path('error/',ErrorView.as_view(),name="error"),
    path('team/',TeamView.as_view(),name="team"),
    
   
    
    
    
    
]
