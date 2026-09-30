from django import forms
from .models import Person, Connection

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'profession', 'interests']
        widgets = {
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['person_from', 'person_to', 'connection_type', 'strength']
        widgets = {
            'strength': forms.RadioSelect(),
            'connection_type': forms.Select(attrs={'class': 'form-select'}),
            'person_from': forms.Select(attrs={'class': 'form-select'}),
            'person_to': forms.Select(attrs={'class': 'form-select'}),
        }