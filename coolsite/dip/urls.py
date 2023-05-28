from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('lecture/<slug:lecture_slug>/', show_lecture, name='lecture'),
    path('laboratory/<slug:laboratory_slug>/', show_laboratory, name='laboratory'),
    path('parabolic/', laboratory_result_parabolic, name='laboratory_result_parabolic'),
    path('hyperbolic/', laboratory_result_hyperbolic, name='laboratory_result_hyperbolic'),
    path('download-pdf/', download_pdf, name='download_pdf'),
    # path('compiler/', compiler, name='compiler'),


    # path('laboratory/compiler/', compiler, name='compiler'),
    # path('laboratory/inaccuracy_and_parameters', show_page_parameters_and_inaccuracy, name='inaccuracy_and_parameters'),
]
