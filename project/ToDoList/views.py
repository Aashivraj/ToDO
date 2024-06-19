from django.shortcuts import render
from django import views 
from .forms import TodoForm, AddUserForm
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


class add_todo(views.View):
   def get(self,request,*args, **kwargs):
       form=TodoForm()
       return render(request, 'admin_templates/add_todo.html',{'form':form})
    
   def post(self,request,*args, **kwargs):
         form=TodoForm(request.POST)
         if form.is_valid():
            form.save()
            return render(request, 'admin_templates/home.html')
         else:
            print(form.errors)
            
            return render(request, 'admin_templates/add_todo.html',{'form':form})


class ErrorView(views.View):   
   def get(self,request,*args, **kwargs):
      return render(request,'admin_templates/error.html')


class AddUserView(views.View):
   def get(self,request,*args, **kwargs):
       form=AddUserForm()
       return render(request, 'admin_templates/add_user.html',{'form':form})
    
   
   def post(self,request,*args, **kwargs):
         form=AddUserForm(request.POST)
         if form.is_valid():
            form.save()
            return render(request, 'admin_templates/home.html')
         else:
            print(form.errors)
            
            return render(request, 'admin_templates/add_user.html',{'form':form})