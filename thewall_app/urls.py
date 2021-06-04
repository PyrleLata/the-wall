from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('add-post', views.add_post),
    path('edit/<int:post_id>', views.edit_post),
    path('modify-post', views.modify_post),
    path('add-comment', views.add_comment),
    path('add-like/<int:post_id>', views.add_like),
    path('delete-post/<int:post_id>', views.delete_post),
    # path('delete-comment/<int:post_id>', views.delete_comment),
]