from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User

from django import forms
from django.core.validators import RegexValidator


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-2',
            'placeholder': 'Введите имя пользователя',
            'id': 'inputUsername'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-2',
            'placeholder': 'Введите пароль',
            'id': 'inputPassword'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Введите имя', }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Введите фамилию', }))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Введите имя пользователя', }))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-2', 'placeholder': 'Введите почту', }))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-2', 'placeholder': 'Введите пароль', }))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-2', 'placeholder': 'Подтвердите пароль', }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control py-2'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True, 'class': 'form-control py-2'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))


    # поле phone с валидацией
    phone = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате: +7 (999) 999-99-99'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control py-2',
            'placeholder': '+7 (999) 999-99-99'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone')
