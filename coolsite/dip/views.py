from django.http import FileResponse, Http404
import math
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.lib import colors
from .forms import *
from .models import *
import plotly.graph_objects as go
from math import cos, exp, sin
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt
import io
import os
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


menu = [{'title': "Компилятор на Python", 'url_name': 'compiler'},
        {'title': "Войти как админ", 'url_name': 'admin'}
]


def index(request):
    posts = Lecture.objects.all()
    return render(request, 'dip/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})


def show_lecture(request, lecture_slug):
    lecture = get_object_or_404(Lecture, slug=lecture_slug)
    posts = Lecture.objects.all()
    context = {'posts': posts, 'lecture': lecture, 'title': lecture.title, 'menu': menu}
    return render(request, 'dip/post_lecture.html', context=context)


def show_laboratory(request, laboratory_slug):
    url = request.path
    url_parts = url.split('/'); desired_part = url_parts[-2] + '/' + url_parts[-1]
    laboratory = get_object_or_404(Lecture, slug=laboratory_slug)
    posts = Lecture.objects.all()

    if desired_part == "parabolic-lekciya/":
        if request.method == 'POST':
            form = PostFormParabolic(request.POST)
            if form.is_valid():
                return redirect('home')
        else:
            form = PostFormParabolic()

        context = {'menu': menu, 'posts': posts, 'laboratory': laboratory, 'form': form}
        return render(request, "dip/post_laboratory_parabolic.html", context)

    elif desired_part == "hyperbolic-lekciya/":
        if request.method == 'POST':
            form = PostFormHyperbolic(request.POST)
            if form.is_valid():
                return redirect('home')
        else: form = PostFormHyperbolic()

        context = {'menu': menu, 'posts': posts, 'laboratory': laboratory, 'form': form}
        return render(request, "dip/post_laboratory_hyperbolic.html", context)

    else: raise Http404("Страница не найдена")


def reverse_diagonal(matrix):
    n = len(matrix); m = len(matrix[0])

    # Создаем новую матрицу с размерами m x n
    reversed_matrix = [[0] * n for _ in range(m)]

    # Переворачиваем значения вдоль диагонали
    for i in range(n):
        for j in range(m):
            reversed_matrix[j][i] = matrix[i][j]

    return reversed_matrix


def draw_for_pdf(l_draw, t_draw, u_draw):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d'); ax.set_facecolor('white')
    l_draw, t_draw = np.meshgrid(l_draw, t_draw)
    surf = ax.plot_surface(l_draw, t_draw, u_draw.T, cmap='coolwarm', linewidth=0, antialiased=False)
    ax.set_xlabel('x', fontsize=14); ax.set_ylabel('t', fontsize=14); ax.set_zlabel('u', fontsize=14)
    return fig


def laboratory_result_parabolic(request):
    if request.method == 'POST':
        n = 10; m = 10; a = 0; b = 1
        u_yav = np.zeros((n + 1, m + 1)); u_neyav = np.zeros((n + 1, m + 1))
        gamma = float(request.POST.get('par_gamma')); small_m = float(request.POST.get('par_m')); alpha = float(request.POST.get('par_alpha'))
        betta = float(request.POST.get('par_betta')); big_M = float(request.POST.get('par_big_M')); big_N = float(request.POST.get('par_big_N'))
        big_S = float(request.POST.get('par_S')); delta = float(request.POST.get('par_delta')); h = (b - a) / n

        def f(x): return gamma * cos(small_m * x)

        def fi1(t): return alpha * t + betta * exp(t)

        def fi2(t): return big_N * t + big_M * sin(small_m * t)

        def yav():
            for i in range(n + 1): u_yav[i, 0] = f(a + i * h)

            for j in range(1, m + 1): u_yav[0, j] = fi1(j * delta * h * h); u_yav[n, j] = fi2(j * delta * h * h)

            for j in range(m):
                for i in range(1, n): u_yav[i, j + 1] = delta * (u_yav[i - 1, j] + 4 * u_yav[i, j] + u_yav[i + 1, j])


        def neyav():
            a1 = np.zeros((n + 1, m)); b1 = np.zeros((n + 1, m))

            for i in range(n + 1): u_neyav[i, 0] = f(a + i * h)

            for j in range(1, m + 1): u_neyav[0, j] = fi1(j * h * h / big_S); u_neyav[n, j] = fi2(j * h * h / big_S)

            for j in range(m):
                a1[1, j] = 1 / (2 + big_S)
                b1[1, j] = fi1((j + 1) * h * h / big_S) + big_S * u_neyav[1, j]

            for i in range(2, n + 1):
                for j in range(m):
                    a1[i, j] = 1 / (2 + big_S - a1[i - 1, j])
                    b1[i, j] = a1[i - 1, j] * b1[i - 1, j] + big_S * u_neyav[i, j]

            for j in range(m):
                for i in range(1, n): u_neyav[i, j + 1] = a1[i, j] * (b1[i, j] + u_neyav[i + 1, j + 1])

        yav(); neyav()

        # создаем двумерные матрицы в виде списков списков
        u_yav_list = [[round(col, 3) for col in row] for row in u_yav.tolist()]
        u_neyav_list = [[round(col, 3) for col in row] for row in u_neyav.tolist()]

        # переворачиваем списки относительно диагонали
        reversed_matrix_yav = reverse_diagonal(u_yav_list)
        reversed_matrix_neyav = reverse_diagonal(u_neyav_list)

        # генерация значений осей
        l = np.linspace(a, b, num=n + 1); t = np.linspace(0, m * delta, num=m + 1)
        l = np.round(l, 2); t = np.round(t, 2)

        # создание интерактивного графика
        fig_yav = go.Figure(data=[go.Surface(z=u_yav.T, colorscale='Viridis')])
        fig_neyav = go.Figure(data=[go.Surface(z=u_neyav.T, colorscale='Viridis')])

        # Настройка осей и меток
        fig_yav.update_layout(
            scene=dict(
                xaxis=dict(title='x', tickvals=np.arange(len(l)), ticktext=l, title_font=dict(size=18)),
                yaxis=dict(title='t', tickvals=np.arange(len(t)), ticktext=t, title_font=dict(size=18)),
                zaxis=dict(title='u', title_font=dict(size=18)),
                aspectratio=dict(x=0.9, y=0.9, z=0.9)),
            autosize=False, width=765, height=550, margin=dict(l=0, r=10, b=0, t=10))

        fig_neyav.update_layout(
            scene=dict(
                xaxis=dict(title='x', tickvals=np.arange(len(l)), ticktext=l, title_font=dict(size=18)),
                yaxis=dict(title='t', tickvals=np.arange(len(t)), ticktext=t, title_font=dict(size=18)),
                zaxis=dict(title='u', title_font=dict(size=18)),
                aspectratio=dict(x=0.9, y=0.9, z=0.9)),
            autosize=False, width=765, height=550, margin=dict(l=0, r=10, b=0, t=10))

        graph_div_yav = fig_yav.to_html(full_html=False, default_height=550, default_width=765)
        graph_div_neyav = fig_neyav.to_html(full_html=False, default_height=550, default_width=765)

        # создание pdf-файла
        buffer = io.BytesIO(); pdf = canvas.Canvas(buffer, pagesize=letter)
        pdfmetrics.registerFont(TTFont('ArialGreek', 'C:/Python/DiplomTTT/ttf/Arial.ttf'))
        pdf.setFont("ArialGreek", 14)
        pdf.drawString(30, 730,
                       f'Начальные параметры для явной схемы решения ДУЧП параболического типа:')
        pdf.drawString(30, 710,
                       f'γ: {gamma},       m: {small_m},       α: {alpha},       β: {betta},       M: {big_M},       N: {big_N},       δ: {delta}')

        # Добавление первого графика в PDF-документ
        graph_yav = draw_for_pdf(l, t, u_yav)
        graph_yav_filename = "graph_yav.png"
        graph_yav_path = os.path.join(settings.MEDIA_ROOT, graph_yav_filename)
        graph_yav.savefig(graph_yav_path, format='png')
        pdf.drawInlineImage(graph_yav_path, 60, 305, width=500, height=400)

        # Добавление таблицы в PDF-документ
        table_data = [['explicit']]  # Добавляем пустую ячейку для номеров строк
        for i, row in enumerate(reversed_matrix_yav):
            table_data.append([str(i)] + [str(j) for j in reversed(row)])

        # Добавление нумерации столбцов
        for i in range(11): table_data[0].append(str(i))

        table = Table(table_data, colWidths=47, rowHeights=18)
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Изменяем размер шрифта для нумерации столбцов
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Выравнивание по центру для нумерации столбцов
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Задаем серый фон для нумерации столбцов
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Задаем белый текст для нумерации столбцов
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Получение размеров таблицы
        table_width, table_height = table.wrap(400, 350)

        # Указание координат таблицы на странице
        table_x = 30; table_y = 300 - table_height

        # Добавление таблицы в PDF-документ
        table.drawOn(pdf, table_x, table_y); pdf.showPage()

        # Неявная схема
        pdf.setFont("ArialGreek", 14)
        pdf.drawString(30, 730,
                       f'Начальные параметры для неявной схемы решения ДУЧП параболического типа:')
        pdf.drawString(30, 710,
                       f'γ: {gamma},       m: {small_m},       α: {alpha},       β: {betta},       M: {big_M},       N: {big_N},       S: {big_S}')

        # Добавление второго графика в PDF-документ
        graph_neyav = draw_for_pdf(l, t, u_neyav)
        graph_neyav_filename = "graph_neyav.png"
        graph_neyav_path = os.path.join(settings.MEDIA_ROOT, graph_neyav_filename)
        graph_neyav.savefig(graph_neyav_path, format='png')
        pdf.drawInlineImage(graph_neyav_path, 60, 305, width=500, height=400)

        # Добавление таблицы в PDF-документ
        table_data = [['implicit']]  # Добавляем пустую ячейку для номеров строк
        for i, row in enumerate(reversed_matrix_neyav):
            table_data.append([str(i)] + [str(j) for j in reversed(row)])

        # Добавление нумерации столбцов
        for i in range(11): table_data[0].append(str(i))

        table = Table(table_data, colWidths=47, rowHeights=18)
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Изменяем размер шрифта для нумерации столбцов
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Выравнивание по центру для нумерации столбцов
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Задаем серый фон для нумерации столбцов
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Задаем белый текст для нумерации столбцов
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Получение размеров таблицы
        table_width, table_height = table.wrap(400, 350)

        # Указание координат таблицы на странице
        table_x = 30; table_y = 300 - table_height

        # Добавление таблицы в PDF-документ
        table.drawOn(pdf, table_x, table_y)

        # Завершение создания PDF-документа
        pdf.showPage(); pdf.save()

        # Удаление временных файлов с графиками
        graph_yav.clf(); graph_neyav.clf()
        os.remove(graph_yav_path); os.remove(graph_neyav_path)

        # Получение данных PDF-файла из буфера
        pdf_buffer = buffer.getvalue(); buffer.close()

        # Сохранение PDF-файла
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result_parabolic.pdf')
        with open(pdf_file_path, 'wb') as file: file.write(pdf_buffer)

        context = {
                'menu': menu, 'graph_yav': graph_div_yav, 'graph_neyav': graph_div_neyav,
                'u_yav': reversed_matrix_yav, 'u_neyav': reversed_matrix_neyav,
                'range_n': list(range(n + 1)), 'range_m': list(range(m + 1)),
                'gamma': gamma, 'small_m': small_m, 'alpha': alpha, 'betta': betta, 'big_M': big_M, 'big_N': big_N, 'big_S': big_S, 'delta': delta
            }
        return render(request, "dip/laboratory_result_parabolic.html", context)

    else:
        raise Http404("Страница не найдена")


def laboratory_result_hyperbolic(request):
    if request.method == 'POST':
        x0 = 0; x1 = 1; n = 10; m = 11; h = (x1 - x0) / n; k = h
        U = np.zeros((n + 1, m)); U_1 = [0.0] * n
        gamma = float(request.POST.get('par_gamma')); small_m = float(request.POST.get('par_m')); alpha = float(request.POST.get('par_alpha'))
        betta = float(request.POST.get('par_betta')); big_M = float(request.POST.get('par_big_M')); big_N = float(request.POST.get('par_big_N'))

        def f(x): return gamma * math.cos(small_m * x)

        def F(x): return alpha + betta * math.sin(small_m * x)

        def fi(t): return alpha * t + betta * math.exp(t)

        def psi(t): return big_N * t + big_M * math.sin(small_m * t)

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

        x = np.linspace(x0, x1, n + 1); t = np.linspace(0, k * (m - 1), m)
        x = np.round(x, 2); t = np.round(t, 2)

        # Создание трехмерной поверхности
        fig = go.Figure(data=[go.Surface(z=U.T, colorscale='Viridis')])

        # Настройка осей и меток
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='x', tickvals=np.arange(len(x)), ticktext=x, title_font=dict(size=18)),
                yaxis=dict(title='t', tickvals=np.arange(len(t)), ticktext=t, title_font=dict(size=18)),
                zaxis=dict(title='u', title_font=dict(size=18)), aspectratio=dict(x=0.9, y=0.9, z=0.9)),
            autosize=False, width=765, height=550, margin=dict(l=0, r=10, b=0, t=10))

        graph_fig = fig.to_html(full_html=False, default_height=550, default_width=765)

        # создание pdf-файла
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdfmetrics.registerFont(TTFont('ArialGreek', 'C:/Python/DiplomTTT/ttf/Arial.ttf'))

        pdf.setFont("ArialGreek", 14)
        pdf.drawString(30, 730,
                       f'Начальные параметры для решения ДУЧП гиперболического типа:')
        pdf.drawString(30, 710,
                       f'γ: {gamma},       m: {small_m},       α: {alpha},       β: {betta},       M: {big_M},       N: {big_N}')

        # Добавление второго графика в PDF-документ
        graph_hyperbolic = draw_for_pdf(x, t, U)
        graph_hyperbolic_filename = "graph_parabolic.png"
        graph_hyperbolic_path = os.path.join(settings.MEDIA_ROOT, graph_hyperbolic_filename)
        graph_hyperbolic.savefig(graph_hyperbolic_path, format='png')
        pdf.drawInlineImage(graph_hyperbolic_path, 60, 305, width=500, height=400)

        # Добавление таблицы в PDF-документ
        # Добавление таблицы в PDF-документ
        table_data = [['implicit']]  # Добавляем пустую ячейку для номеров строк
        for i, row in enumerate(reversed_matrix_results):
            table_data.append([str(i)] + [str(j) for j in reversed(row)])

        # Добавление нумерации столбцов
        for i in range(11): table_data[0].append(str(i))

        table = Table(table_data, colWidths=47, rowHeights=18)
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Изменяем размер шрифта для нумерации столбцов
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Выравнивание по центру для нумерации столбцов
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Задаем серый фон для нумерации столбцов
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Задаем белый текст для нумерации столбцов
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Получение размеров таблицы
        table_width, table_height = table.wrap(400, 350)

        # Указание координат таблицы на странице
        table_x = 30; table_y = 300 - table_height

        # Добавление таблицы в PDF-документ
        table.drawOn(pdf, table_x, table_y)

        # Завершение создания PDF-документа
        pdf.showPage(); pdf.save()

        # Удаление временных файлов с графиками
        graph_hyperbolic.clf(); os.remove(graph_hyperbolic_path)

        # Получение данных PDF-файла из буфера
        pdf_buffer = buffer.getvalue(); buffer.close()

        # Сохранение PDF-файла
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result_hyperbolic.pdf')
        with open(pdf_file_path, 'wb') as file: file.write(pdf_buffer)

        context = {
            'menu': menu, 'graph_fig': graph_fig, 'u_hyperbolic': reversed_matrix_results, 'range_m': range(m),
            'gamma': gamma, 'small_m': small_m, 'alpha': alpha, 'betta': betta, 'big_M': big_M, 'big_N': big_N}
        return render(request, 'dip/laboratory_result_hyperbolic.html', context)

    else:
        # Обработка GET-запроса
        return HttpResponse("Invalid request method")


def download_pdf_parabolic(request):
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result_parabolic.pdf')  # Путь к PDF-файлу
    with open(pdf_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    return response


def download_pdf_hyperbolic(request):
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'result_hyperbolic.pdf')  # Путь к PDF-файлу
    with open(pdf_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result_hyperbolic.pdf"'
    return response


def compiler(request):
    posts = Lecture.objects.all()
    context = {'menu': menu, 'posts': posts,}
    return render(request, 'dip/compiler.html', context=context)