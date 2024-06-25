import django_filters
import django_filters.widgets
from .models import Todo
from django import forms
from django_filters import DateFilter
from django.contrib.auth.models import *
from .models import CustomUser  # Import your custom user model



class TodoFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(
        lookup_expr='icontains',
        widget=forms.DateInput(
            attrs={
                'id': 'datepicker',
                'type': 'text',
                'class': 'datepicker theme-sensitive'  # Add a class to target the date picker
            }
        )
    )
   
    class Meta:
        model = Todo
        fields = ['user', 'date_created', 'team']
        
        
        
class TeamTodoFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(
        lookup_expr='icontains',
        widget=forms.DateInput(
            attrs={
                'id': 'datepicker',
                'type': 'text',
                'class': 'datepicker theme-sensitive'  # Add a class to target the date picker
            }
        )
    )

    class Meta:
        model = Todo
        fields = ['user', 'date_created']
        
        
    user = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.none())
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the logged-in user from the kwargs
        super(TeamTodoFilter, self).__init__(*args, **kwargs)
        
        if user:
            # Assuming the CustomUser model has a ForeignKey to the Team model
            user_team = user.team  
            self.filters['user'].queryset = CustomUser.objects.filter(team=user_team).exclude(id=user.id)
            
            
            