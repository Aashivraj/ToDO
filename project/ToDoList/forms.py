from django import forms
from .models import *


class TeamForm(forms.ModelForm):
    team_department = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Team Department',
                'id': 'user_team_department',
            }
        )
    )

    class Meta:
        model = Team
        fields = '__all__'
class CustomUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields='__all__'
        
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'note', 'status', 'user', 'team']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 4,
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note',
                'rows': 2,
            }),
            'status': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'team': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TodoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['team'].initial = user.team if user.team else None
  
class AddUserForm(forms.ModelForm):
    user_name = forms.CharField(
        required=False,  # Remove HTML5 required
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'User Name',
                'id': 'customuser_username',
            }
        )
    )
    email = forms.EmailField(
        required=False,  # Remove HTML5 required
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'id': 'customuser_email',
            }
        )
    )
    mobile_number = forms.CharField(
        required=False,  # Remove HTML5 required
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
        required=False,  # Remove HTML5 required
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'customuser_team',
            }
        )
    )
    role = forms.ChoiceField(
        required=False,  # Remove HTML5 required
        choices=[
            ('3', 'Developer'),  # Default choices
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if user.role == '1':  # Admin
                self.fields['role'].choices = [
                    ('2', 'TeamLeader')
                ]
            elif user.role == '2':  # TeamLeader
                self.fields['role'].choices = [
                    ('3', 'Developer')
                ]
                
 

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
