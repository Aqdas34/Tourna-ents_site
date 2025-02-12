from django import forms
from .models import Tournament
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import datetime



class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'event_name', 'date', 'location', 'age_group', 'gender',
            'event_type', 'style', 'flyer_url', 'club_name', 
            'tournament_director', 'contact_info'
        ]
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Event Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'age_group': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'style': forms.Select(attrs={'class': 'form-select'}),
            'flyer_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Flyer URL'}),
            'club_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Club Name'}),
            'tournament_director': forms.Select(attrs={'class': 'form-select'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Info', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Save Tournament'))

    def clean_flyer_url(self):
        flyer_url = self.cleaned_data.get('flyer_url')
        if flyer_url and not flyer_url.startswith("http"):
            raise forms.ValidationError("Flyer URL must start with 'http' or 'https'.")
        return flyer_url

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past.")
        return date
