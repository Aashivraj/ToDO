from django import forms
from .models import *

class TeamForm(forms.ModelForm):
    class Meta:
      model=Team
      fields='__all__'
      
class CustomUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields='__all__'
        
class TodoForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "title",
                "class": "form-control",
                "id":"todo_title" ,
               
                
            }
        ))
    status = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "status",
                "class": "form-control",
                "id":"todo_status" ,
               
                
            }
        ))
    date_created = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "placeholder": "date_created",
                "class": "form-control",
                "id":"todo_created" ,
               
                
            }
        ))
     
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "note",
                "class": "form-control",
                "id":"desc" ,
                "aria-describedby":"emailHelp" ,
                "rows":2
                
            }
        ))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "description",
                "class": "form-control",
                "id":"desc" ,
                "aria-describedby":"emailHelp" ,
                "rows":2
                
            }
        ))
    class Meta:
        model=Todo
        fields=('user', 'title','description','status','date_created','note')
        
class AddUserForm(forms.ModelForm):
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'User Name',
                'id': 'customuser_username',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'id': 'customuser_email',
            }
        )
    )
    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number',
                'id': 'customuser_mobile_number',
            }
        )
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'customuser_team',
            }
        ),
        required=False  # Assuming team is optional (null=True, blank=True)
    )

    role = forms.ChoiceField(
        choices=[
            ('1', 'Admin'),
            ('2', 'TeamLeader'),
            ('3', 'Developer'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'customuser_role',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('user_name', 'email', 'mobile_number', 'team', 'role')
        
        

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
