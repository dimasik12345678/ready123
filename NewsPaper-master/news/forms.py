from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from allauth.account.forms import SignupForm

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
            min_length=15,
            widget=forms.Textarea({'cols': 70, 'rows': 2})
    )
    text = forms.CharField(
            min_length=150,
            widget=forms.Textarea({'cols': 70, 'rows': 7})
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            # 'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if title == text:
            raise ValidationError(
                    'Текст не должен совпадать с заголовком!'
            )
        return cleaned_data


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
