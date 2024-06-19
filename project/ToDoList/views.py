from django.shortcuts import render
from django import views 
# Create your views here.
class login(views.View):
    def get(self,request,*args, **kwargs):
       return render(request, 'templates/login.html')
   
class register(views.View):
    def get(self,request,*args, **kwargs):
       return render(request, 'templates/register.html')
   
class home(views.View):
    def get(self,request,*args, **kwargs):
       return render(request, 'templates/home.html')


class ErrorView(views.View):   
   def get(self,request,*args, **kwargs):
      return render(request,'templates/error.html')
