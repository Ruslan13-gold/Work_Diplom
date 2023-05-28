from django import forms
from .models import *

class PostFormParabolic(forms.Form):
    # Параметры метода
    par_gamma = forms.CharField(max_length=3, label=u"\u03B3: ", widget=forms.TextInput(
        attrs={'name': 'par_gamma',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'title': 'Ошибка ввода',
               }))

    par_m = forms.CharField(max_length=255, label="m: ", widget=forms.TextInput(
        attrs={'name': 'par_m',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_alpha = forms.CharField(max_length=255, label="\u03B1: ", widget=forms.TextInput(
        attrs={'name': 'par_alpha',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_betta = forms.CharField(max_length=255, label="\u03B2: ", widget=forms.TextInput(
        attrs={'name': 'par_betta',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_big_M = forms.CharField(max_length=255, label="M: ", widget=forms.TextInput(
        attrs={'name': 'par_big_M',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_big_N = forms.CharField(max_length=255, label="N: ", widget=forms.TextInput(
        attrs={'name': 'par_big_N',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_S = forms.CharField(max_length=255, label="S: ", widget=forms.TextInput(
        attrs={'name': 'par_big_N',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_delta = forms.CharField(max_length=255, label="\u03b4: ", widget=forms.TextInput(
        attrs={'name': 'par_big_N',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))


class PostFormHyperbolic(forms.Form):
    # Параметры метода
    par_gamma = forms.CharField(max_length=3, label=u"\u03B3: ", widget=forms.TextInput(
        attrs={'name': 'par_gamma',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'title': 'Ошибка ввода',
               }))

    par_m = forms.CharField(max_length=255, label="m: ", widget=forms.TextInput(
        attrs={'name': 'par_m',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_alpha = forms.CharField(max_length=255, label="\u03B1: ", widget=forms.TextInput(
        attrs={'name': 'par_alpha',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_betta = forms.CharField(max_length=255, label="\u03B2: ", widget=forms.TextInput(
        attrs={'name': 'par_betta',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_big_M = forms.CharField(max_length=255, label="M: ", widget=forms.TextInput(
        attrs={'name': 'par_big_M',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))

    par_big_N = forms.CharField(max_length=255, label="N: ", widget=forms.TextInput(
        attrs={'name': 'par_big_N',
               'class': 'custom_input',
               'placeholder': '0.1',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',

               'title': 'Ошибка ввода',
               }))