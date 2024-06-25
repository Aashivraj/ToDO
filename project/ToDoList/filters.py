       import django_filters
import django_filters.widgets
from .models import Todo
from django import forms
from django_filters import DateFilter


class TodoFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(
        lookup_expr='icontains',
        widget=forms.DateInput(
            attrs={
                'id': 'datepicker',
                'type': 'text'
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
                'type': 'text'
            }
        )
    )
   

    class Meta:
        model = Todo
        fields = ['user', 'date_created']


