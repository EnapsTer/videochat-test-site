"""forms.py"""
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment, Profile


class PostCreateForm(forms.ModelForm):
    """post creation form"""
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'class': 'form-control w-100'}))
    private = forms.BooleanField(
        required=False, label='Make post private', widget=forms.CheckboxInput(
        ))
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """meta class"""
        model = Post
        fields = (
            'title',
            'body',
            'private'
        )


class PostEditForm(forms.ModelForm):
    """post editing form"""
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Title', 'class': 'form-control w-100'}))
    body = forms.CharField(widget=CKEditorUploadingWidget())
    private = forms.BooleanField(
        required=False, label='Make post private: ', widget=forms.CheckboxInput(
        ))

    class Meta:
        """meta class"""
        model = Post
        fields = (
            'title',
            'body',
            'private'
        )


class UserLoginForm(forms.Form):
    """login form"""
    username = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control w-100'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control w-100'}))


class UserRegistrationForm(forms.ModelForm):
    """registration form"""
    username = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control w-100'}))
    first_name = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'form-control w-100'}))
    last_name = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'form-control w-100'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your email', 'class': 'form-control w-100'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password here', 'class': 'form-control w-100'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password', 'class': 'form-control w-100'}))

    class Meta:
        """meta class"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )

    def clean_confirm_password(self):
        """check password"""
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords are not equal')
        return confirm_password


class UserEditForm(forms.ModelForm):
    """user edit form"""
    username = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control w-100'}))
    first_name = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': 'form-control w-100'}))
    last_name = forms.CharField(max_length=20, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'class': 'form-control w-100'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'form-control w-100'}))

    class Meta:
        """meta class"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CommentForm(forms.ModelForm):
    """comment form"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """meta class"""
        model = Comment
        fields = {'content'}


class ProfileForm(forms.ModelForm):
    """profile form"""
    class Meta:
        """meta class"""
        model = Profile
        exclude = ('user',)
