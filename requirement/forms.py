from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

class RequirementForm(forms.Form):
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class' : 'validate'}))
    requirements = forms.CharField(required=True, widget=forms.Textarea(attrs={'class' : 'materialize-textarea', 'id': 'id_requirements'}))

    error = None

    def clean(self):
        data = super().clean()

        if not data.get('title'):
            self.error = 'Please fill title'
            raise ValidationError('Missing title')
        elif not data.get('requirements'):
            self.error = 'Please fill requirements'
            raise ValidationError('Missing requirements')
        else:
            self.error = None
