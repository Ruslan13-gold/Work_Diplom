import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *

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

        # создаем двумерную матрицу в виде списка списков
        u_list = [[round(col, 3) for col in row] for row in u.tolist()]
        reversed_matrix = reverse_diagonal(u_list)


        # отрисовка графика
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('white')
        l = np.linspace(a, b, num=n + 1)
        t = np.linspace(0, m * delta, num=m + 1)
        l, t = np.meshgrid(l, t)
        surf = ax.plot_surface(l, t, u.T, cmap='coolwarm', linewidth=0, antialiased=False)
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('t', fontsize=14)
        ax.set_zlabel('u', fontsize=14)
        graph_path = os.path.join(settings.MEDIA_ROOT, 'graph.png')
        plt.savefig(graph_path)

        context = {
            'graph_url': '/media/graph.png',
            'n': n,
            'm': m,
            'u': reversed_matrix,
            'range_n': list(range(n + 1)),
            'range_m': list(range(m + 1))
        }

        return render(request, "dip/laboratory_result.html", context)