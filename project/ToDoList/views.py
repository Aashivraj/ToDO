from django.shortcuts import render,redirect
from django import views 
from .forms import TodoForm, AddUserForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

   

@login_required(login_url="/login/")   
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
         
         
         
         
class LoginFormView(views.View):
   def get(self,request,*args, **kwargs):
      form=LoginForm()
      return render(request, 'admin_templates/login.html')
    
   def post(self,request,*args, **kwargs):
      form = LoginForm(request.POST or None)

  

   

      if form.is_valid():
            username = form.cleaned_data.get("username")
            print("sdfasd",username)
            password = form.cleaned_data.get("password")
            user = authenticate(user_name=username, password=password)
            if user is not None:
                print("asdfasdfa",user)
                login(request, user)
                return redirect("/home/")
            else:
               print(form.errors)
               return redirect("login")
      else:
            print(form.errors)


      return render(request, "admin_templates/login.html", {"form": form})

@login_required(login_url="/login/")
def Logoutpage(request):
    logout(request)
    return redirect('login')
