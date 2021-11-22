from django.urls import path
from .api import user_all_api_view, user_create_api_view, user_by_id_api_view, user_update_password_api_view

urlpatterns = [
    path(
        'all/',
        user_all_api_view,
        name='user_list_all'
    ),
    path(
        'create/',
        user_create_api_view,
        name='user_create'
    ),
    path(
        'id/<int:id>',
        user_by_id_api_view,
        name='user_by_id'
    ),
    path(
        'password/<int:id>',
        user_update_password_api_view,
        name='user_password_update'
    ),
]
