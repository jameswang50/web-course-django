from django.urls import path

from .views import (
    savollar,
    savol_detail,
    check_answer,
    create_question,
    create_choice,
    c_choice
)


app_name = 'poll'
urlpatterns = [
    path('', savollar, name="savollar"),
    path('savol/<int:id>/', savol_detail, name="savol"),
    path('check/<int:variant_id>/', check_answer, name="check_answer"),
    path('savol-yaratish/', create_question, name="create"),
    path('tanlov-yaratish/', create_choice, name="create_choice"),
    path(
        'savolga-tanlov-yaratish/<int:savol_id>',
        c_choice, name="savolga_tanlov")
]
