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
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "customuser",
            }
        )
    )
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