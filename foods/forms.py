from django import forms
from .models import Image,Comment

class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','about']
        lables = {'image':'','about':''}
        widgets = {'about':forms.Textarea(attrs={'rows':4,'cols':40})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        lables = {'comment':''}
        widgets = {'comment':forms.Textarea(attrs={'rows':3,'cols':40})}
