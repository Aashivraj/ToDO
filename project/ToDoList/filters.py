import django_filters
from .models import Todo
from django import forms
from django_filters import DateFilter

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
