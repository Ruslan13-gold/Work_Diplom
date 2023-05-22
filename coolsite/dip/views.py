from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *

# <table id="result-table">
#
#   {% for row in u %}
#     <tr>
#       {% for col in row %}
#         <td>{{ col }}</td>
#       {% endfor %}
#     </tr>
#   {% endfor %}
#
# </table>

import pandas as pd
from tabulate import tabulate
from math import cos, exp, sin
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


menu = ['О сайте', 'Добавить статью', 'Войти']


def index(request):
    posts = Lecture.objects.all()
    return render(request, 'dip/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})


def about(request):
    return render(request, 'dip/about.html', {'menu': menu, 'title': 'About'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_lecture(request, lecture_slug):
    lecture = get_object_or_404(Lecture, slug=lecture_slug)
    posts = Lecture.objects.all()

    context = {
        'posts': posts,
        'lecture': lecture,
        'title': lecture.title,
    }

    return render(request, 'dip/post_lecture.html', context=context)


def show_laboratory(request, laboratory_slug):
    laboratory = get_object_or_404(Lecture, slug=laboratory_slug)
    posts = Lecture.objects.all()
    # form = PostFormAddFunctionAndSection()
    if request.method == 'POST':
        form = PostFormAddFunctionAndSection(request.POST)
        if form.is_valid():
            return redirect('home')
        else:
            return redirect('laboratory')
    else:
        form = PostFormAddFunctionAndSection()

    context = {
        'posts': posts,
        'laboratory': laboratory,
        'form': form,
    }

    return render(request, 'dip/post_laboratory.html', context=context)


def laboratory_result(request):
    if request.method == 'POST':
        n = 10
        m = 10
        a = 0
        b = 1
        u = np.zeros((n + 1, m + 1))
        gamma = float(request.POST.get('par_gamma'))
        small_m = float(request.POST.get('par_m'))
        alpha = float(request.POST.get('par_alpha'))
        betta = float(request.POST.get('par_betta'))
        big_M = float(request.POST.get('par_big_M'))
        big_N = float(request.POST.get('par_big_N'))
        big_S = float(request.POST.get('par_S'))
        delta = float(request.POST.get('par_delta'))
        h = (b - a) / n

        def f(x):
            return gamma * cos(small_m * x)

        def fi1(t):
            return alpha*t + betta * exp(t)

        def fi2(t):
            return big_N * t + big_M * sin(small_m * t)

        def yav():
            for i in range(n + 1):
                u[i, 0] = f(a + i * h)

            for j in range(1, m + 1):
                u[0, j] = fi1(j * delta * h * h)
                u[n, j] = fi2(j * delta * h * h)

            for j in range(m):
                for i in range(1, n):
                    u[i, j + 1] = delta * (u[i - 1, j] + 4 * u[i, j] + u[i + 1, j])

        def neyav():
            a1 = np.zeros((n + 1, m))
            b1 = np.zeros((n + 1, m))

            for i in range(n + 1):
                u[i, 0] = f(a + i * h)

            for j in range(1, m + 1):
                u[0, j] = fi1(j * h * h / big_S)
                u[n, j] = fi2(j * h * h / big_S)

            for j in range(m):
                a1[1, j] = 1 / (2 + big_S)
                b1[1, j] = fi1((j + 1) * h * h / big_S) + big_S * u[1, j]

            for i in range(2, n + 1):
                for j in range(m):
                    a1[i, j] = 1 / (2 + big_S - a1[i - 1, j])
                    b1[i, j] = a1[i - 1, j] * b1[i - 1, j] + big_S * u[i, j]

            for j in range(m):
                for i in range(1, n):
                    u[i, j + 1] = a1[i, j] * (b1[i, j] + u[i + 1, j + 1])

        yav()

        def reverse_diagonal(matrix):
            n = len(matrix)
            m = len(matrix[0])

            # Создаем новую матрицу с размерами m x n
            reversed_matrix = [[0] * n for _ in range(m)]

            # Переворачиваем значения вдоль диагонали
            for i in range(n):
                for j in range(m):
                    reversed_matrix[j][i] = matrix[i][j]

            return reversed_matrix

        # u_list = u.tolist()  # Преобразование массива numpy в список
        u_list = [[round(col, 3) for col in row] for row in u.tolist()]
        reversed_matrix = reverse_diagonal(u_list)

        context = {
            'n': n,
            'm': m,
            'u': reversed_matrix,
            'range_n': list(range(n + 1)),
            'range_m': list(range(m + 1))
        }

        return render(request, "dip/laboratory_result.html", context)




# def compiler(request):
#     posts = Lecture.objects.all()
#
#     context = {
#         'posts': posts,
#     }
#
#     return render(request, 'dip/compiler.html', context=context)

# def show_page_parameters_and_inaccuracy(request, laboratory_id):
#     posts = Lecture.objects.all()
#     laboratory = get_object_or_404(Lecture, pk=laboratory_id)
#     if request.method == 'POST':
#         form = FormParametersAndInaccuracy(request.POST)
#         if form.is_valid():
#             return redirect('inaccuracy_and_parameters')
#         else:
#             return redirect('laboratory')
#     else:
#         form = FormParametersAndInaccuracy()
#
#     context = {
#         'posts': posts,
#         'form': form,
#     }
#
#     return render(request, 'dip/parameters_and_inaccuracy.html', context=context)