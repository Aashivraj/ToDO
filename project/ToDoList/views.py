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
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash





# Create your views here.
def user_is_admin(user):
    return user.is_authenticated and user.role == "1"






class ChangePasswordView(views.View,LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = 'admin_templates/change_password.html'
    success_url = reverse_lazy('password_change_done')

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password has been changed successfully.')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})


       
class UpdateTodoComment(LoginRequiredMixin, views.View):


    

    def get(self,request,id,*args, **kwargs):
        data=Todo.objects.get(pk=id)
        form=UpdateTodoForm(instance=data)
        context={
            'form':form,
        }
        return render(request,'admin_templates/update_todo_comment.html',context)
        
            
            
    def post(self,request,id,*args, **kwargs):
        data=Todo.objects.get(pk=id)
      
        form=UpdateTodoForm(request.POST,instance=data)
        
        if form.is_valid():
            if 'date_created' in form.changed_data:
                form.instance.date_created = data.date_created  
            form.save()
            return redirect('todolist')
        
        return render(request,'admin_templates/update_todo_comment.html',{'form':form})
        
        
class ToggleActiveStatusView(LoginRequiredMixin, views.View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.toggle_active_status()
        messages.success(request, 'user active status change')
        
        return redirect(('userlist'))


class TeamLeadView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        # Check if user is authenticated and has role equal to 2
        if not user.is_authenticated or user.role != "2":
            return render(request, 'admin_templates/error.html')  # Custom 403 Forbidden page
        
        team1 = user.team
        
        # Filter Todo objects based on team
        todos = Todo.objects.filter(
            Q(team=team1)
        ).exclude(user=user).order_by('status')
        
        # Apply filters if GET parameters are present
        todo_filter = TeamTodoFilter(request.GET, queryset=todos, user=user)
        todos = todo_filter.qs

        # Calculate time taken for each todo item
        for todo in todos:
            if todo.update_time and todo.date_created:
                time_difference = todo.update_time - todo.date_created
                hours, remainder = divmod(time_difference.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                todo.time_taken = f"{int(hours)}h {int(minutes)}m"
            else:
                todo.time_taken = "N/A"
        
        return render(request, 'teamleader_templates/teamtodo.html', {'todos': todos, 'todo_filter': todo_filter})
   
   
  
class home(LoginRequiredMixin, views.View):
    
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.role == "1":
            user = request.user
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
                for todo in pending_todos:
                    if todo.update_time and todo.date_created:
                        time_difference = todo.update_time - todo.date_created
                        hours, remainder = divmod(time_difference.total_seconds(), 3600)
                        minutes, _ = divmod(remainder, 60)
                        todo.time_taken = f"{int(hours)}h {int(minutes)}m"
                    else:
                        todo.time_taken = "N/A"
                team_todos[team] = pending_todos

            context = {
                'team_todos': team_todos,
                'todos': todos,
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


class add_todo(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("User not authenticated", status=401)
        user = request.user
        form = TodoForm(user=user)
        return render(request, 'admin_templates/add_todo.html', {'form': form, 'user': user})
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = TodoForm(request.POST, user=user)  # Initialize form with POST data and user
        
        # Check if form is valid and handle errors
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.team = user.team
            todo.save()
            messages.success(request, 'Todo added')
            return redirect('home')  # Redirect to home page after successful form submission
        else:
            # Add error messages for specific fields if they are empty
            if 'title' not in form.cleaned_data or not form.cleaned_data['title']:
                messages.error(request, 'Please enter a title.')
            if 'description' not in form.cleaned_data or not form.cleaned_data['description']:
                messages.error(request, 'Please enter a description.')
            if 'note' not in form.cleaned_data or not form.cleaned_data['note']:
                messages.error(request, 'Please enter a note.')
            
            return render(request, 'admin_templates/add_todo.html', {'form': form, 'user': user})

class update_todo(LoginRequiredMixin, views.View):
        
    def post(self, request, todo_id):  # Add 'self' as the first parameter
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        new_status = request.POST.get('status')
        if new_status:
            todo.status = int(new_status)
            todo.update_time = timezone.now()  # Update the current time
            todo.save()
            messages.success(request, 'Task Updated')
            
        
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
               # Only superusers can set the team
           
            
            if not user_name:
                messages.error(request, 'Username cannot be blank')
                return render(request, 'admin_templates/add_user.html', {'form': form})
            if not email:
                messages.error(request, 'Email cannot be blank')
                return render(request, 'admin_templates/add_user.html', {'form': form})
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format')
                return render(request, 'admin_templates/add_user.html', {'form': form})
                
            
                    
        
            if not mobile_number:
                messages.error(request, 'Mobile number cannot be blank')
                return render(request, 'admin_templates/add_user.html', {'form': form})
            
            if not request.user.is_superuser:
                # Set team to current user's team if not a superuser
                team = request.user.team
            else:
                team = form.cleaned_data['team']
            if not team :
                messages.error(request, 'Team cannot be blank for admin users')
                return render(request, 'admin_templates/add_user.html', {'form': form})
          
            
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
                    messages.success(request, f'Welcome, {username}!')
                    
                    
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



    
class UpdateUserView(LoginRequiredMixin, views.View):
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
        
        
       
class DeleteUserView(LoginRequiredMixin, views.View) :
    def get(self, request,id,*args, **kwargs):
        delete_user=CustomUser.objects.get(pk=id)
        delete_user.delete()
        messages.success(request, 'User Deleted Successfully')
        
        return redirect('userlist')
      
            
class ToDoListView(views.View):
    template_name = 'admin_templates/todo_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        filters = None
        
        if user.role == "1":
            queryset = Todo.objects.all()
            todos = queryset.order_by('status')
            filters = TodoFilter(request.GET, queryset=todos)
            todos = filters.qs
        elif user.role == "2" or user.role == "3":
            todos = Todo.objects.filter(user=user).order_by('status')
        
        # Calculate time_taken for each todo item
        for todo in todos:
            if todo.update_time and todo.date_created:
                time_difference = todo.update_time - todo.date_created
                hours, remainder = divmod(time_difference.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                todo.time_taken = f"{int(hours)}h {int(minutes)}m"
            else:
                todo.time_taken = "N/A"

        return render(request, self.template_name, {'todos': todos, 'filter': filters})



 
@method_decorator(user_passes_test(user_is_admin), name='dispatch')   
class TeamView(views.View):
    
    def get(self, request, *args, **kwargs):
        team_form=TeamForm()
      
        return render(request, 'admin_templates/team_form.html', {'team_form': team_form})
    def post(self, request, *args, **kwargs):
        team_form=TeamForm(request.POST)
       
        
            
        if team_form.is_valid():
            department = team_form.cleaned_data.get("team_department")
            if Team.objects.filter(team_department=department).exists():
                messages.warning(request, 'Team already taken')
                return redirect('team')
            
            team = Team(
                team_department=department,
            
            )
           
            team.save()
            
            return redirect('add_user')
        else:
            if 'team_department' not in team_form.cleaned_data or not team_form.cleaned_data['team_department']:
                messages.error(request, 'Please enter a Team.')
            return render(request, 'admin_templates/team_form.html', {'team_form': team_form})
    
class AdminHomeTodoView(LoginRequiredMixin, views.View):
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
    
class ProfilePageView(LoginRequiredMixin, views.View):
    template_name = 'admin_templates/profile.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            username = request.user
            profile_images_dir = os.path.join(settings.MEDIA_ROOT, 'profile_images')
            
            # Delete old profile picture if it exists
            if request.user.photo:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, str(request.user.photo))
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
                    messages.warning(request, 'profile pic removed')
                    
            
            # Ensure the directory exists
            if not os.path.exists(profile_images_dir):
                os.makedirs(profile_images_dir)

            # Save new profile picture
            fs = FileSystemStorage(location=profile_images_dir)
            filename = f'{username}.png'  # Save as username.png
            filename = fs.save(filename, profile_picture)
            request.user.photo = 'profile_images/' + filename
            request.user.save()
            messages.success(request, 'profile pic added')
            
            return redirect('profile')  # Redirect to the profile page or any other appropriate page
        
        # If no profile_picture in request.FILES, render the template
        return render(request, self.template_name)
    
class SettingsView(LoginRequiredMixin, views.View):
    template_name = 'admin_templates/settings.html'

    def get(self, request, *args, **kwargs):
        system_settings = SystemSettings.objects.first()
        company_logo_url = None
        small_logo_url = None
        
        if system_settings:
            if system_settings.company_logo:
                company_logo_url = settings.MEDIA_URL + system_settings.company_logo
            if system_settings.small_logo:
                small_logo_url = settings.MEDIA_URL + system_settings.small_logo
        
        return render(request, self.template_name, {
            'system_settings': system_settings,
            'company_logo_url': company_logo_url,
            'small_logo_url': small_logo_url,
        })

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
                    messages.warning(request, 'Logo is removed')
            
            # Determine the file extension and save the new logo
            file_extension = logo.name.split('.')[-1]
            filename = 'Systemlogo.' + file_extension
            fs = FileSystemStorage(location=logo_dir)
            filename = fs.save(filename, logo)
            
            if system_settings:
                system_settings.company_logo = 'logo/' + filename
                system_settings.save()
                messages.warning(request, 'New logo added')
            else:
                # Create a new SystemSettings instance if it doesn't exist
                SystemSettings.objects.create(company_logo='logo/' + filename)
        
        if 'small_logo' in request.FILES:
            small_logo = request.FILES['small_logo']
            small_logo_dir = os.path.join(settings.MEDIA_ROOT, 'logo')
            
            # Ensure the directory exists
            if not os.path.exists(small_logo_dir):
                os.makedirs(small_logo_dir)
            
            # Delete the old small logo if it exists
            if system_settings and system_settings.small_logo:
                old_small_logo_path = os.path.join(settings.MEDIA_ROOT, system_settings.small_logo)
                if os.path.exists(old_small_logo_path):
                    os.remove(old_small_logo_path)
                    messages.warning(request, 'Small Logo is removed')
            
            # Save the new small logo
            small_filename = 'small_logo.png'  # Fixed filename for small logo
            fs = FileSystemStorage(location=small_logo_dir)
            small_filename = fs.save(small_filename, small_logo)
            
            if system_settings:
                system_settings.small_logo = 'logo/' + small_filename
                system_settings.save()
                messages.warning(request, 'New small logo added')
            else:
                # Create a new SystemSettings instance if it doesn't exist
                SystemSettings.objects.create(small_logo='logo/' + small_filename)
        
        else:
            # Handle other form fields update here
            if system_settings:
                system_settings.company_name = request.POST.get('company_name', system_settings.company_name)
                system_settings.mobile = request.POST.get('mobile', system_settings.mobile)
                system_settings.email = request.POST.get('email', system_settings.email)
                system_settings.facebook = request.POST.get('facebook', system_settings.facebook)
                system_settings.instagram = request.POST.get('instagram', system_settings.instagram)
                system_settings.linkdein = request.POST.get('linkdein', system_settings.linkdein)
                system_settings.company_link = request.POST.get('company_link', system_settings.company_link)
                
                system_settings.save()
                messages.warning(request, 'Data updated')
        
        return redirect('system_settings')

        
class TaskDetailView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        user_id = kwargs.get('user_role')

        current_user = request.user

        if current_user.role == "1":
            # User with role 1 can see all tasks
            task = get_object_or_404(Todo, id=task_id)
            
        elif current_user.role == "2":
            # User with role 2 can see tasks of their team members
            team_members = CustomUser.objects.filter(team=current_user.team)
            if Todo.objects.filter(id=task_id, user__in=team_members).exists():
                task = get_object_or_404(Todo, id=task_id)
            else:
                return render(request, 'admin_templates/forbiddenerror.html')
                
        elif current_user.role == "3":
            # User with role 3 can only see their own tasks
            if Todo.objects.filter(id=task_id, user=current_user).exists():
                task = get_object_or_404(Todo, id=task_id)
            else:
                return render(request, 'admin_templates/forbiddenerror.html')
                
        else:
            # For any other user, deny access
            return render(request, 'admin_templates/forbiddenerror.html')

        context = {
            'task': task,
            'can_view_task': True,
        }
        return render(request, 'admin_templates/individual_todo.html', context)
     
def system_settings(request):
    # Assuming SystemSettings has a unique instance or you fetch the appropriate settings
    system_settings = SystemSettings.objects.first()  # Fetch your SystemSettings object
    return {'system_settings': system_settings}
        
