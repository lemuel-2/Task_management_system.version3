from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'priority', 'due_date', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'e.g. Update API documentation'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional description…'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_completed'}),
        }
