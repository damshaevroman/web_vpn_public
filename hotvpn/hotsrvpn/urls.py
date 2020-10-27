from django.urls import path, re_path

from hotsrvpn.views_user import *
from hotsrvpn.views_hotel import *

urlpatterns = [
    # user pages urls
    path('user/', render_user_main_page),
    path('user/create_user/', create_user, name='create_user'),
    path('user/edit_user/<int:id>/', show_edit_user_page),
    path('user/save_edit_user_form/', save_edit_user_form, name='save_edit_user_form'),
    path('user/delete_user/', delete_user, name="delete_user"),
    path('user/create_user_certificate/', create_user_certificate, name="create_certificate"),
    path('user/copy_certificate_to_host/', copy_certificate_to_host, name="copy_certificate_to_host"),
    path('user/render_user_json/', render_user_json, name="render_user_json"),
    path('user/get_user_json/', render_user_json, name="render_user_json"),


    path('hotel/', render_hotel_main_page),
    path('hotel/create_hotel/', create_hotel_view, name='create_hotel'),
    path('hotel/edit_hotel/<int:id>', show_edit_hotel_page),
    path('hotel/save_edit_hotel_form/', save_edit_hotel_form, name='save_edit_hotel_form'),
    path('hotel/delete_hotel/', delete_hotel, name="delete_hotel"),
    path('hotel/create_hotel_certificate/', create_hotel_certificate, name="create_hotel_certificate"),
    path('hotel/get_status_cerificate/', get_status_cerificate, name="get_status_cerificate"),
    path('hotel/copy_certificate_to_host/', copy_certificate_to_host, name="copy_certificate_to_host"),
    path('hotel/get_json/', render_hotel_json, name="render_hotel_json"),

    path('create_vpn_server/', create_vpn_server),

]
