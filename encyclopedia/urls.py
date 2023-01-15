from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.entry_page, name='entry_page'),
    path("search", views.search, name="search"),
    path("new", views.new_page, name="new_page")
]
