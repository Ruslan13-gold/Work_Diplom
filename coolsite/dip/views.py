import os
import tempfile
from django.http import FileResponse, Http404
import math
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
import plotly.graph_objects as go
from math import cos, exp, sin
import numpy as np
import io
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt
from django.shortcuts import render
import asyncio
import io
import os
import tempfile
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


menu = ['О сайте', 'Добавить статью', 'Войти']


def index(request):
    posts = Lecture.objects.all()
    return render(request, 'dip/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})


def about(request):
    return render(request, 'dip/about.html', {'menu': menu, 'title': 'About'})


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
    url = request.path
    url_parts = url.split('/')
    desired_part = url_parts[-2] + '/' + url_parts[-1]
    laboratory = get_object_or_404(Lecture, slug=laboratory_slug)
    posts = Lecture.objects.all()

    if desired_part == "parabolic-lekciya/":
        if request.method == 'POST':
            form = PostFormParabolic(request.POST)
            if form.is_valid():
                return redirect('home')
        else:
            form = PostFormParabolic()

        context = {
            'posts': posts,
            'laboratory': laboratory,
            'form': form,
        }
        return render(request, "dip/post_laboratory_parabolic.html", context)

    elif desired_part == "hyperbolic-lekciya/":
        if request.method == 'POST':
            form = PostFormHyperbolic(request.POST)
            if form.is_valid():
                return redirect('home')
        else:
            form = PostFormHyperbolic()

        context = {
            'posts': posts,
            'laboratory': laboratory,
            'form': form,
        }
        return render(request, "dip/post_laboratory_hyperbolic.html", context)

    else:
        raise Http404("Страница не найдена")


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


def draw_for_pdf(l_draw, t_draw, u_draw):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')
    l_draw, t_draw = np.meshgrid(l_draw, t_draw)
    surf = ax.plot_surface(l_draw, t_draw, u_draw.T, cmap='coolwarm', linewidth=0, antialiased=False)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('t', fontsize=14)
    ax.set_zlabel('u', fontsize=14)
    return fig


def laboratory_result_parabolic(request):
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

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Добавление первого графика в PDF-документ
        graph_yav = draw_for_pdf(l, t, u_yav)
        graph_yav_filename = "graph_yav.png"
        graph_yav_path = os.path.join(settings.MEDIA_ROOT, graph_yav_filename)
        graph_yav.savefig(graph_yav_path, format='png')

        pdf.drawInlineImage(graph_yav_path, 30, 400, width=500, height=350)

        # Добавление второго графика в PDF-документ
        graph_neyav = draw_for_pdf(l, t, u_neyav)
        graph_neyav_filename = "graph_neyav.png"
        graph_neyav_path = os.path.join(settings.MEDIA_ROOT, graph_neyav_filename)
        graph_neyav.savefig(graph_neyav_path, format='png')

        pdf.drawInlineImage(graph_neyav_path, 30, 30, width=500, height=350)

        # Добавление таблицы в PDF-документ
        table_data = [['x', 't', 'u_yav']]
        for i, row in enumerate(reversed_matrix_yav):
            table_data.append([str(i)] + [str(j) for j in row])

        table = Table(table_data, colWidths=50, rowHeights=20)
        table.setStyle(TableStyle([
            # Стили таблицы...
        ]))
        table.wrapOn(pdf, 500, 300)
        table.drawOn(pdf, 30, 750)

        # Завершение создания PDF-документа
        pdf.showPage()
        pdf.save()

        # Удаление временных файлов с графиками
        graph_yav.clf()
        graph_neyav.clf()
        os.remove(graph_yav_path)
        os.remove(graph_neyav_path)

        # Получение данных PDF-файла из буфера
        pdf_buffer = buffer.getvalue()
        buffer.close()

        # Сохранение PDF-файла
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result.pdf')
        with open(pdf_file_path, 'wb') as file:
            file.write(pdf_buffer)

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

        return render(request, "dip/laboratory_result_parabolic.html", context)

    else:
        raise Http404("Страница не найдена")


def laboratory_result_hyperbolic(request):
    if request.method == 'POST':
        x0 = 0
        x1 = 1
        n = 10
        m = 11
        h = (x1 - x0) / n
        k = h

        U = np.zeros((n + 1, m))
        U_1 = [0.0] * n
        gamma = float(request.POST.get('par_gamma'))
        small_m = float(request.POST.get('par_m'))
        alpha = float(request.POST.get('par_alpha'))
        betta = float(request.POST.get('par_betta'))
        big_M = float(request.POST.get('par_big_M'))
        big_N = float(request.POST.get('par_big_N'))

        def f(x):
            return gamma * math.cos(small_m * x)

        def F(x):
            return alpha + betta * math.sin(small_m * x)

        def fi(t):
            return alpha * t + betta * math.exp(t)

        def psi(t):
            return big_N * t + big_M * math.sin(small_m * t)

        def hyperbolic_decision():
            for i in range(n + 1):
                U[i][0] = f(x0 + i * h)

            for j in range(m):
                U[0][j] = fi(j * k)
                U[n][j] = psi(j * k)

            for i in range(1, n):
                U_1[i] = U[i][0] - k * F(x0 + i * h)
                U[i][1] = U[i + 1][0] + U[i - 1][0] - U_1[i]

            for j in range(1, m - 1):
                for i in range(1, n):
                    U[i][j + 1] = U[i + 1][j] + U[i - 1][j] - U[i][j - 1]

        hyperbolic_decision()
        results = [[round(col, 3) for col in row] for row in U.tolist()]
        reversed_matrix_results = reverse_diagonal(results)

        x = np.linspace(x0, x1, n + 1)
        t = np.linspace(0, k * (m - 1), m)
        x = np.round(x, 2)
        t = np.round(t, 2)

        # Создание трехмерной поверхности
        fig = go.Figure(data=[go.Surface(z=U.T, colorscale='Viridis')])

        # Настройка осей и меток
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    title='x',
                    tickvals=np.arange(len(x)),
                    ticktext=x,
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

        graph_fig = fig.to_html(full_html=False, default_height=550, default_width=765)

        context = {
            'graph_fig': graph_fig,
            'u_yav': reversed_matrix_results,
            'range_m': range(m),
            'gamma': gamma,
            'small_m': small_m,
            'alpha': alpha,
            'betta': betta,
            'big_M': big_M,
            'big_N': big_N,
        }
        return render(request, 'dip/laboratory_result_hyperbolic.html', context)

    else:
        # Обработка GET-запроса
        return HttpResponse("Invalid request method")


def download_pdf(request):
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result.pdf')  # Путь к PDF-файлу

    with open(pdf_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'

    return response


# def compiler(request):
#     posts = Lecture.objects.all()
#
#     context = {
#         'posts': posts,
#     }
#
#     return render(request, 'dip/compiler.html', context=context)


