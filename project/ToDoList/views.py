from django.shortcuts import get_object_or_404, render,redirect
from django import views
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class teamlead(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        # Check if user is authenticated and has role equal to 2
        if not user.is_authenticated or user.role != "2":
            # Redirect or handle unauthorized access
            # For example, you can redirect to login or show a permission denied page
            return render(request, 'admin_templates/error.html')  # Custom 403 Forbidden page
        
        today = timezone.now().date()  # Get today's date
        team1 = user.team
        userid = user.id
        print(userid)
        
        # Filter Todo objects based on team
        todo = Todo.objects.filter(
            Q(team=team1) &
            (Q(date_created__date=today) | Q(status=0))
        ).exclude(user__id=userid).order_by('status')
        
        return render(request, 'teamleader_templates/teamtodo.html', {'todo': todo})

   
  
class home(LoginRequiredMixin, views.View):
    
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.role == "1":
            teams = Team.objects.all()
            team_todos = {}
            for team in teams:
                pending_todos = Todo.objects.filter(team=team, status=0)
                team_todos[team] = pending_todos

            context = {
                'team_todos': team_todos,
            }
            return render(request, 'admin_templates/home.html', context)
        
        if user.role == "2":
            user = self.request.user
            users=CustomUser.objects.filter(
                Q(team=user.team)
            )
            today = timezone.now().date()  # Get today's date
            todos = Todo.objects.filter(
                Q(user=user) & 
                (Q(date_created__date=today) | Q(status=0))
            )  # Fetch todos for the authenticated user
            
            form = TodoForm()

            return render(request, 'admin_templates/home.html',{'form': form, 'users':users,'todos': todos})   

        else:
            user = self.request.user
            today = timezone.now().date()  # Get today's date
            todos = Todo.objects.filter(
                Q(user=user) & 
                (Q(date_created__date=today) | Q(status=0))
            )  # Fetch todos for the authenticated user
            
            form = TodoForm()
            return render(request, 'admin_templates/home.html', {'form': form, 'todos': todos})


class add_todo(LoginRequiredMixin,views.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("User not authenticated", status=401)
        user = request.user
        form = TodoForm(user=user)
        return render(request, 'admin_templates/add_todo.html', {'form': form, 'user': user})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = TodoForm(request.POST, user=user)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.team = user.team
            todo.save()
            return redirect('home')  # Assuming 'home' is the name of the URL for the home page
        else:
            return render(request, 'admin_templates/add_todo.html', {'form': form, 'user': user})

class update_todo(LoginRequiredMixin, views.View):
        
    def post(self, request, todo_id):  # Add 'self' as the first parameter
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        new_status = request.POST.get('status')
        if new_status:
            todo.status = int(new_status)
            todo.save()
        
        return redirect('home')  # Redirect to the home page after updating status

class ErrorView(LoginRequiredMixin,views.View):   
   def get(self,request,*args, **kwargs):
      return render(request,'admin_templates/error.html')


class AddUserView(LoginRequiredMixin,views.View):
    def get(self, request, *args, **kwargs):
        form = AddUserForm(user=request.user)
        return render(request, 'admin_templates/add_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddUserForm(request.POST, user=request.user)
        
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
    
   def post(self, request, *args, **kwargs):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        print("sdfasd", username)
        password = form.cleaned_data.get("password")
        user = authenticate(user_name=username, password=password)

        if user is not None:
            if user.is_active:
                print("asdfasdfa", user)
                login(request, user)
                return redirect("/home/")
            else:
                print("User is not active.")
                return redirect("login")
        else:
            print("Invalid credentials.")
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
        user = request.user
        
        print(user.role)

        if user.role == "1":
            # Admin: view all ToDo items
            todos = Todo.objects.all().order_by('status')
        
        elif user.role == "5":
            # Team Leader: view ToDo items for their team, excluding their own
            team1 = user.team
            userid = user.id

            todos = Todo.objects.filter(
                Q(team=team1)
            ).exclude(user__id=userid).order_by('status')
        
        else:
            # Regular User: view only their ToDo items
            todos = Todo.objects.filter(user=user).order_by('status')
        
        return render(request, self.template_name, {'todos': todos})
 
 
    
class TeamView(views.View):
    def get(self, request, *args, **kwargs):
        team_form=TeamForm()
      
        return render(request, 'admin_templates/team_form.html', {'team_form': team_form})
    def post(self, request, *args, **kwargs):
        team_form=TeamForm(request.POST)
        if team_form.is_valid():
            team_form.save()
            return redirect('add_user')
        return render(request, 'admin_templates/team_form.html', {'team_form': team_form})
    
class AdminHomeTodoView(views.View):
    template_name = 'admin_templates/todo_list.html'
    
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()  # Fetch all teams
        
        print(teams)
        team_todos = {}
        
        for team in teams:
            todos = Todo.objects.filter(team=team).order_by('status')
            team_todos[team] = todos
            
            print(team)
        
        return render(request, self.template_name, {'team_todos': team_todos})   