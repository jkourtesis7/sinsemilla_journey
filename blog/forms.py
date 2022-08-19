from django import forms
from . import models
class ExampleSignupForm(forms.Form):
    """Example Signup Form"""
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.EmailField()
    gender = forms.ChoiceField(
        label='Gender',
        required=False,
        choices=[
            (None, '-------'),
            ('m', 'Male'),
            ('f','Female'),
            ('n', 'Non-binary'),
        ]
    )
    receive_newsletter = forms.BooleanField(
        required=False,
        label='Do you wish to receive our newsletter?'
    )

class CommentForm(forms.ModelForm):
    """ Comment Form """
    class Meta:
        model = models.Comment
        fields = [
            'post',
            'name',
            'email',
            'text',
        ]
        labels = {
            'text': 'Comment'
        }
        widgets = {
            'post': forms.HiddenInput()
        }
