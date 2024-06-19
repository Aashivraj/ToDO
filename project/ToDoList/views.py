from django.shortcuts import render
from django import views 
from .forms import TodoForm
# Create your views here.
class login(views.View):
    def get(self,request,*args, **kwargs):
       return render(request, 'admin_templates/login.html')
   
class register(views.View):
    def get(self,request,*args, **kwargs):
       return render(request, 'admin_templates/register.html')
   
class home(views.View):
    def get(self,request,*args, **kwargs):
   
       return render(request, 'admin_templates/home.html')


class add_user(views.View):
    def get(self,request,*args, **kwargs):
       form=TodoForm()
       return render(request, 'admin_templates/add_user.html',{'form':form})


class ErrorView(views.View):   
   def get(self,request,*args, **kwargs):
      return render(request,'admin_templates/error.html')


