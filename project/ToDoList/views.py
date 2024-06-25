from django.shortcuts import get_object_or_404, render,redirect
from django import views
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .filters import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.



class ToggleActiveStatusView(views.View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.toggle_active_status()
        return redirect(('userlist'))


class TeamLeadView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        # Check if user is authenticated and has role equal to 2
        if not user.is_authenticated or user.role != "2":
            return render(request, 'admin_templates/error.html')  # Custom 403 Forbidden page
        
        today = timezone.now().date()  # Get today's date
        team1 = user.team
        
        # Filter Todo objects based on team
        todo_list = Todo.objects.filter(
            Q(team=team1)
        ).exclude(user=user).order_by('status')
        
        # Apply filters if GET parameters are present
        todo_filter = TeamTodoFilter(request.GET, queryset=todo_list, user=user)
        todo_list = todo_filter.qs
        
        return render(request, 'teamleader_templates/teamtodo.html', {'todo_list': todo_list, 'todo_filter': todo_filter})
   
  
class home(LoginRequiredMixin, views.View):
    
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.role == "1":
            teams = Team.objects.all()
            today = timezone.now().date()  # Get today's date
            todos = Todo.objects.filter(
                Q(user=user) & 
                (Q(date_created__date=today) | Q(status=0))
            )  # Fetch todos for the authenticated user
            form = TodoForm()
            team_todos = {}
            for team in teams:
                pending_todos = Todo.objects.filter(team=team, status=0)
                team_todos[team] = pending_todos

            context = {
                'team_todos': team_todos,
                'todos': todos,
            }
            return render(request, 'admin_templates/home.html', context )
        
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
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'admin_templates/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect("/home/")
                else:
                    messages.warning(request, 'User is not active.')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Form is not valid')

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
        queryset = Todo.objects.all()

        if user.role == "1":
            # Admin: view all ToDo items
            todos = queryset.order_by('status')
        elif user.role == "5":
            # Team Leader: view ToDo items for their team, excluding their own
            todos = queryset.filter(
                Q(team=user.team)
            ).exclude(user__id=user.id).order_by('status')
        else:
            # Regular User: view only their ToDo items
            todos = queryset.filter(user=user).order_by('status')

        filter = TodoFilter(request.GET, queryset=todos)
        todos = filter.qs

        return render(request, self.template_name, {'todos': todos, 'filter': filter})


 
    
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
    
class TeamToDo(views.View):
    template_name = 'teamleader_templates/teamtodo.html'
    
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
    

class ProfilePageView(views.View):
    template_name = 'admin_templates/profile.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            profile_images_dir = os.path.join(settings.MEDIA_ROOT, 'profile_images')

            # Ensure the directory exists
            if not os.path.exists(profile_images_dir):
                os.makedirs(profile_images_dir)

            fs = FileSystemStorage(location=profile_images_dir)
            filename = fs.save(profile_picture.name, profile_picture)
            request.user.photo = 'profile_images/' + filename
            request.user.save()
            return redirect('profile')  # Redirect to the profile page or any other appropriate page
        return render(request, self.template_name)
    
class SettingsView(views.View):
    template_name = 'admin_templates/settings.html'

    def get(self, request, *args, **kwargs):
            system_settings = SystemSettings.objects.first()
            company_logo_url = None
            if system_settings and system_settings.company_logo:
                company_logo_url = settings.MEDIA_URL + system_settings.company_logo
        
            return render(request, self.template_name, {'system_settings': system_settings, 'company_logo_url': company_logo_url})

    def post(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()
        if 'logo' in request.FILES:
            logo = request.FILES['logo']
            logo_dir = os.path.join(settings.MEDIA_ROOT, 'logo')

            # Ensure the directory exists
            if not os.path.exists(logo_dir):
                os.makedirs(logo_dir)

            # Delete the old logo if it exists
            if system_settings and system_settings.company_logo:
                old_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.company_logo)
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)

            # Determine the file extension and save the new logo
            file_extension = logo.name.split('.')[-1]
            filename = 'Systemlogo.' + file_extension
            fs = FileSystemStorage(location=logo_dir)
            filename = fs.save(filename, logo)

            if system_settings:
                system_settings.company_logo = 'logo/' + filename
                system_settings.save()
            else:
                # Create a new SystemSettings instance if it doesn't exist
                SystemSettings.objects.create(company_logo='logo/' + filename)

            return redirect('system_settings')                   
            
        else:
            system_settings.company_name = request.POST.get('company_name', system_settings.company_name)
            system_settings.mobile = request.POST.get('mobile', system_settings.mobile)
            system_settings.email = request.POST.get('email', system_settings.email)
            system_settings.facebook = request.POST.get('facebook', system_settings.facebook)
            system_settings.instagram = request.POST.get('instagram', system_settings.instagram)
            system_settings.linkdein = request.POST.get('linkdein', system_settings.linkdein)
            system_settings.company_link = request.POST.get('company_link', system_settings.company_link)
            
            system_settings.save()
        
            return redirect('system_settings')
        
class TaskDetailView(views.View):
     def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        task_id = kwargs.get('task_id')
        task = get_object_or_404(Todo, id=task_id, user_id=user_id)
        context = {
            'task': task,
        }
        return render(request, 'admin_templates/individual_todo.html', context)