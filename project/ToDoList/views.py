from django.shortcuts import render,redirect
from django import views

from .models import *
from .forms import TodoForm, AddUserForm,LoginForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

   
  
class home(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        todos = Todo.objects.filter(user=user)  # Fetch todos for the authenticated user
        form = TodoForm()
        return render(request, 'admin_templates/home.html', {'form': form, 'todos': todos})


class add_todo(LoginRequiredMixin,views.View):
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


class ErrorView(LoginRequiredMixin,views.View):   
   def get(self,request,*args, **kwargs):
      return render(request,'admin_templates/error.html')


class AddUserView(LoginRequiredMixin,views.View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'admin_templates/add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST, request.FILES)
        
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            mobile_number = form.cleaned_data['mobile_number']
            team = form.cleaned_data['team']
            role = form.cleaned_data['role']
            
         

            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'Email already taken')
                return redirect('add_user')
            if CustomUser.objects.filter(user_name=user_name).exists():
                messages.warning(request, 'Username already taken')
                return redirect('add_user')

            user = CustomUser(
                user_name=user_name,
                email=email,
                mobile_number=mobile_number,
                team=team,
                role=role,
                
            )
            user.set_password(request.POST.get('user_name'))
            user.save()

            messages.success(request, 'User successfully added')
            return redirect('add_user')
        else:
            messages.error(request, 'Invalid form data')

        return render(request, 'admin_templates/add_user.html', {'form': form})

         
         
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

class LogoutView(LoginRequiredMixin,views.View):
   def get(self,request,*args, **kwargs):
      logout(request)
      return redirect("login")
  
  

class UserListView(LoginRequiredMixin,views.View):
    def get(self,request,*args, **kwargs):
        users=CustomUser.objects.all()
    
        #paginator
   
        context={
            
            'users':users,
        }

    
        return render(request, 'admin_templates/user_list.html',context)



    
class UpdateUserForm(views.View):
    def get(self,request,id,*args, **kwargs):
        data=CustomUser.objects.get(pk=id)
        form=AddUserForm(instance=data)
        context={
            'form':form,
        }
        return render(request,'admin_templates/update_user.html',context)
        
            
            
    def post(self,request,id,*args, **kwargs):
        data=CustomUser.objects.get(pk=id)
        form=AddUserForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('userlist')
        return render(request,'admin_templates/update_user.html',{'form':form})
        
        
       
class DeleteUserView(views.View) :
    def get(self, request,id,*args, **kwargs):
        delete_user=CustomUser.objects.get(pk=id)
        delete_user.delete()
        return redirect('userlist')

class ToDoListView(views.View):
    template_name = 'admin_templates/todo_list.html'

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.all()  # You can filter or order this query as needed
        context = {
            'todos': todos
        }
        return render(request, self.template_name, context)