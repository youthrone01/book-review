from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add_books),
    url(r'^books/(?P<book_id>[0-9]+)$', views.show_book),
    url(r'^users/(?P<user_id>[0-9]+)$', views.show_user),
    url(r'^users/register$', views.user_register),
    url(r'^users/login$', views.user_login),
    url(r'^delete/(?P<review_id>[0-9]+)$', views.delete),
]
