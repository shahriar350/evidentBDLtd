from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('add/input/', views.InputSave.as_view(), name="add_input"),
    path('input/all/', views.get_whole_data, name="whole_input"),
    path('search/input/<int:input>/', views.InputSearch.as_view(), name="add_search")
]
