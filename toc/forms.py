# forms.py (pour un formulaire de contact potentiel lié aux services)
from django import forms

class ContactServiceForm(forms.Form):
    """
    Formulaire de contact pour les services
    """
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg',
            'placeholder': 'Votre nom'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg',
            'placeholder': 'Votre email'
        })
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg',
            'placeholder': 'Votre message',
            'rows': 4
        })
    )