import os
import tempfile
from django.http import FileResponse
from django.conf import settings

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
import plotly.graph_objects as go
from math import cos, exp, sin
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
from django.shortcuts import render

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
        u_yav = np.zeros((n + 1, m + 1))
        u_neyav = np.zeros((n + 1, m + 1))
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
            return alpha * t + betta * exp(t)

        def fi2(t):
            return big_N * t + big_M * sin(small_m * t)

        def yav():
            for i in range(n + 1):
                u_yav[i, 0] = f(a + i * h)

            for j in range(1, m + 1):
                u_yav[0, j] = fi1(j * delta * h * h)
                u_yav[n, j] = fi2(j * delta * h * h)

            for j in range(m):
                for i in range(1, n):
                    u_yav[i, j + 1] = delta * (u_yav[i - 1, j] + 4 * u_yav[i, j] + u_yav[i + 1, j])

        def neyav():
            a1 = np.zeros((n + 1, m))
            b1 = np.zeros((n + 1, m))

            for i in range(n + 1):
                u_neyav[i, 0] = f(a + i * h)

            for j in range(1, m + 1):
                u_neyav[0, j] = fi1(j * h * h / big_S)
                u_neyav[n, j] = fi2(j * h * h / big_S)

            for j in range(m):
                a1[1, j] = 1 / (2 + big_S)
                b1[1, j] = fi1((j + 1) * h * h / big_S) + big_S * u_neyav[1, j]

            for i in range(2, n + 1):
                for j in range(m):
                    a1[i, j] = 1 / (2 + big_S - a1[i - 1, j])
                    b1[i, j] = a1[i - 1, j] * b1[i - 1, j] + big_S * u_neyav[i, j]

            for j in range(m):
                for i in range(1, n):
                    u_neyav[i, j + 1] = a1[i, j] * (b1[i, j] + u_neyav[i + 1, j + 1])

        yav()
        neyav()

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

        # создаем двумерные матрицы в виде списков списков
        u_yav_list = [[round(col, 3) for col in row] for row in u_yav.tolist()]
        u_neyav_list = [[round(col, 3) for col in row] for row in u_neyav.tolist()]
        reversed_matrix_yav = reverse_diagonal(u_yav_list)
        reversed_matrix_neyav = reverse_diagonal(u_neyav_list)

        l = np.linspace(a, b, num=n + 1)
        t = np.linspace(0, m * delta, num=m + 1)
        l = np.round(l, 2)
        t = np.round(t, 2)

        fig_yav = go.Figure(data=[go.Surface(z=u_yav.T, colorscale='Viridis')])
        fig_neyav = go.Figure(data=[go.Surface(z=u_neyav.T, colorscale='Viridis')])

        fig_yav.update_layout(
            scene=dict(
                xaxis=dict(
                    title='x',
                    tickvals=np.arange(len(l)),
                    ticktext=l,
                    title_font=dict(size=18)
                ),
                yaxis=dict(
                    title='t',
                    tickvals=np.arange(len(t)),
                    ticktext=t,
                    title_font=dict(size=18)
                ),
                zaxis=dict(
                    title='u',
                    title_font=dict(size=18)
                ),
                aspectratio=dict(x=0.9, y=0.9, z=0.9)
            ),
            autosize=False,
            width=765,
            height=550,
            margin=dict(
                l=0, r=10, b=0, t=10
            )
        )

        fig_neyav.update_layout(
            scene=dict(
                xaxis=dict(
                    title='x',
                    tickvals=np.arange(len(l)),
                    ticktext=l,
                    title_font=dict(size=18)
                ),
                yaxis=dict(
                    title='t',
                    tickvals=np.arange(len(t)),
                    ticktext=t,
                    title_font=dict(size=18)
                ),
                zaxis=dict(
                    title='u',
                    title_font=dict(size=18)
                ),
                aspectratio=dict(x=0.9, y=0.9, z=0.9)
            ),
            autosize=False,
            width=765,
            height=550,
            margin=dict(
                l=0, r=10, b=0, t=10
            )
        )

        graph_div_yav = fig_yav.to_html(full_html=False, default_height=550, default_width=765)
        graph_div_neyav = fig_neyav.to_html(full_html=False, default_height=550, default_width=765)

        plt.plot(l, t, u_yav.T)
        plt.xlabel('x')
        plt.ylabel('t')
        plt.title('График результата вычислений')
        plt.grid(True)

        # Сохранение графика во временном файле
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.savefig(tmpfile.name, format='png')

        # Создание PDF-документа
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)

        # Добавление графика в PDF-документ
        pdf.drawInlineImage(tmpfile.name, 30, 400, width=500, height=350)

        # Добавление таблицы в PDF-документ
        table_data = [['x', 't', 'u_yav']]
        for i, row in enumerate(reversed_matrix_yav):
            table_data.append([str(i)] + [str(j) for j in row])

        table = Table(table_data, colWidths=50, rowHeights=20)
        table.setStyle(TableStyle([
            # Стили таблицы...
        ]))
        table.wrapOn(pdf, 500, 300)
        table.drawOn(pdf, 30, 30)

        # Завершение создания PDF-документа
        pdf.showPage()
        pdf.save()

        # Закрытие временного файла
        tmpfile.close()

        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result.pdf')
        with open(pdf_file_path, 'wb') as file:
            file.write(buffer.getvalue())

        context = {
            'pdf_data': pdf_file_path,
            'graph_yav': graph_div_yav,
            'graph_neyav': graph_div_neyav,
            'u_yav': reversed_matrix_yav,
            'u_neyav': reversed_matrix_neyav,
            'range_n': list(range(n + 1)),
            'range_m': list(range(m + 1)),
            'gamma': gamma,
            'small_m': small_m,
            'alpha': alpha,
            'betta': betta,
            'big_M': big_M,
            'big_N': big_N,
            'big_S': big_S,
            'delta': delta
        }

        return render(request, "dip/laboratory_result.html", context)


def download_pdf(request):
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result.pdf')  # Путь к PDF-файлу

    with open(pdf_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'

    return response