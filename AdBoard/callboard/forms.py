from django import forms

from .models import *
from django_ckeditor_5.widgets import CKEditor5Widget


class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['content'].required = False

    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}, config_name='extends'),
        }


class RespondForm(forms.ModelForm):
    class Meta:
        model = Respond
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
