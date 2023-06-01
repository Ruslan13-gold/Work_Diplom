from django.urls import path
from .views import *
from django.contrib import admin


urlpatterns = [
    path('', index, name='home'),
    path('lecture/<slug:lecture_slug>/', show_lecture, name='lecture'),
    path('laboratory/<slug:laboratory_slug>/', show_laboratory, name='laboratory'),
    path('parabolic/', laboratory_result_parabolic, name='laboratory_result_parabolic'),
    path('hyperbolic/', laboratory_result_hyperbolic, name='laboratory_result_hyperbolic'),
    path('download-pdf-parabolic/', download_pdf_parabolic, name='download_pdf_parabolic'),
    path('download-pdf-hyperbolic/', download_pdf_hyperbolic, name='download_pdf_hyperbolic'),
    path('compiler/', compiler, name='compiler'),
    path('grappelli/', admin.site.urls, name='admin'),
    path('error', page_404, name='page_404')
]
