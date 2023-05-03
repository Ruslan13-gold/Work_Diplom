from django import forms
from .models import *

class PostFormAddFunctionAndSection(forms.Form):

    # Функция
    function = forms.CharField(max_length=255, label="Введите уравнение: ", widget=forms.TextInput(
        attrs={'name': 'function',
               'class': 'custom_input',
               'placeholder': '2*x^n',

                '''
                простейшая валидация на стороне клиента
                '''
               'pattern': '[a-z0-9.*^()+-=/]{1,100}',
               'title': 'Ошибка ввода',
               }))


    # Отрезок
    section = forms.CharField(max_length=255, label="Введите отрезок: ", widget=forms.TextInput(
        attrs={'placeholder': '[-1.5;2]',
               'class': 'custom_input',

                '''
                простейшая валидация на стороне клиента
                '''
               'pattern': '[0-9.;-\\[\\]]{1,20}',
               'name': 'section',
               'title': 'Ошибка ввода',
               }))


    # Параметры метода
    par_small = forms.CharField(max_length=255, label=u"\u03bc: ", widget=forms.TextInput(
        attrs={'class': 'custom_input',
               'placeholder': '0.01',

               '''
                простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'name': 'par_small',
               'title': 'Ошибка ввода',
               }))

    par_step = forms.CharField(max_length=255, label="h: ", widget=forms.TextInput(
        attrs={'placeholder': '0.0001',
               'class': 'custom_input',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'name': 'par_step',
               'title': 'Ошибка ввода',
               }))


    # Погрешности метода
    pogr_eps = forms.CharField(max_length=255, label=u"\u03b5: ", widget=forms.TextInput(
        attrs={'class': 'custom_input',
               'placeholder': '0.0001',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'name': 'pogr_eps',
               'title': 'Ошибка ввода',
               }))

    pogr_delta = forms.CharField(max_length=255, label=u"\u03b4: ", widget=forms.TextInput(
        attrs={'placeholder': '0.0001',
               'class': 'custom_input',

               '''
               простейшая валидация на стороне клиента
               '''
               'pattern': '[0-9-.]{1,10}',
               'name': 'pogr_delta',
               'title': 'Ошибка ввода',
               }))


# class FormParametersAndInaccuracy(forms.Form):
#
#     # Параметры метода
#     par_small = forms.CharField(max_length=255, label=u"\u03bc: ", widget=forms.TextInput(
#         attrs={'class': 'custom_input',
#                'placeholder': '2*x^n',
#                }))
#
#     par_step = forms.CharField(max_length=255, label="h: ", widget=forms.TextInput(
#         attrs={'placeholder': '[-1.5;2]',
#                'class': 'custom_input',
#                }))
#
#
#     # Погрешности метода
#     pogr_eps = forms.CharField(max_length=255, label=u"\u03b5: ", widget=forms.TextInput(
#         attrs={'class': 'custom_input',
#                'placeholder': '2*x^n',
#                }))
#
#     pogr_delta = forms.CharField(max_length=255, label=u"\u03b4: ", widget=forms.TextInput(
#         attrs={'placeholder': '[-1.5;2]',
#                'class': 'custom_input',
#                }))