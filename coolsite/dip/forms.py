from django import forms
from .models import *

class PostFormAddFunctionAndSection(forms.Form):

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

    # # Функция
    # function = forms.CharField(max_length=255, label="Введите уравнение: ", widget=forms.TextInput(
    #     attrs={'name': 'function',
    #            'class': 'custom_input',
    #            'placeholder': '2+x^n',
    #            '''
    #            простейшая валидация на стороне клиента
    #            '''
    #            'pattern': '[a-z0-9.*^()+-=/]{1,100}',
    #            'title': 'Ошибка ввода',
    #            }))
    #
    # # Отрезок
    # section = forms.CharField(max_length=255, label="Введите отрезок: ", widget=forms.TextInput(
    #     attrs={'placeholder': '[-1.5;2]',
    #            'class': 'custom_input',
    #
    #            '''
    #            простейшая валидация на стороне клиента
    #            '''
    #            'pattern': '[0-9.;-\\[\\]]{1,20}',
    #            'name': 'section',
    #            'title': 'Ошибка ввода',
    #            }))


    # Погрешности метода
    # pogr_eps = forms.CharField(max_length=255, label=u"\u03b5: ", widget=forms.TextInput(
    #     attrs={'class': 'custom_input',
    #            'placeholder': '0.0001',
    #
    #            '''
    #            простейшая валидация на стороне клиента
    #            '''
    #            'pattern': '[0-9-.]{1,10}',
    #            'name': 'pogr_eps',
    #            'title': 'Ошибка ввода',
    #            }))
    #
    # pogr_delta = forms.CharField(max_length=255, label=u"\u03b4: ", widget=forms.TextInput(
    #     attrs={'placeholder': '0.0001',
    #            'class': 'custom_input',
    #
    #            '''
    #            простейшая валидация на стороне клиента
    #            '''
    #            'pattern': '[0-9-.]{1,10}',
    #            'name': 'pogr_delta',
    #            'title': 'Ошибка ввода',
    #            }))





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