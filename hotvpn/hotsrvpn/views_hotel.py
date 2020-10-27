from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import Hotels_form
from hotsrvpn.businesslogic.hotel_edit import Hotel_edit
import json, os, logging
from hotsrvpn.businesslogic.serializer import HotelSerializer


@login_required(login_url='/')
def render_hotel_main_page(request):
    hotel_form = Hotels_form()
    hotel_edit = Hotel_edit()
    hotel_edit.get_database()
    return render(request, 'hotsrvpn/hotel/hotel_vpn_table.html', {"hotel_form": hotel_form})


"""Get data from Form and add to database Hotel table"""


def create_hotel_view(request):
    if request.is_ajax and request.method == "POST":
        form = Hotels_form(request.POST)
        hotel_add = Hotel_edit()
        if form.is_valid():
            hotel_admin_id = form.cleaned_data.get("hotel_admin_id")
            hotel_country = form.cleaned_data.get("hotel_country")
            hotel_city = form.cleaned_data.get("hotel_city")
            hotel_name = form.cleaned_data.get("hotel_name")
            hotel_name_certification = form.cleaned_data.get("hotel_name_certification")
            hotel_name_certification = hotel_name_certification.replace(' ', '')
            hotel_ip_address = form.cleaned_data.get("hotel_ip_address")
            hotel_port = form.cleaned_data.get("hotel_port")
            hotel_context = {"hotel_country": hotel_country,
                             "hotel_city": hotel_city,
                             "hotel_name": hotel_name,
                             "hotel_name_certification": hotel_name_certification,
                             "hotel_admin_id": hotel_admin_id,
                             "hotel_ip_address": hotel_ip_address,
                             "hotel_port": hotel_port}
            result = hotel_add.write_hotel_to_database(hotel_context)
            hotel_add.get_database()
            return JsonResponse({"result": result}, status=200)

        else:
            errors = hotel_add.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


'''в данном блоке загружаю файл с именами и ip адресами в из файла в словарь и потом ищу по полю short_name ip 
address '''


def show_edit_hotel_page(request, id):
    status_certificate = Hotel_edit()
    result = status_certificate.check_ip_vpn_address(id)
    hotel_form = Hotels_form()
    hotel, check_certeficate_status = status_certificate.edit_hotel_page(id)
    return render(request, "hotsrvpn/hotel/edit_hotel.html",
                  {"result": result, "hotel": hotel, "hotel_form": hotel_form,
                   "check_certeficate_status": check_certeficate_status})


''' get information from HTML page edti_user (form -  save_edit_hotel_form) change and save infortation to database table Hotel'''


def save_edit_hotel_form(request):
    if request.is_ajax and request.method == "POST":
        form = Hotels_form(request.POST)
        hotel_save = Hotel_edit()
        if form.is_valid():
            hotel_admin_id = form.cleaned_data.get("hotel_admin_id")
            hotel_country = form.cleaned_data.get("hotel_country")
            hotel_city = form.cleaned_data.get("hotel_city")
            hotel_name = form.cleaned_data.get("hotel_name")
            hotel_name_certification = form.cleaned_data.get("hotel_name_certification")
            hotel_name_certification = hotel_name_certification.replace(' ', '')
            hotel_ip_address = form.cleaned_data.get("hotel_ip_address")
            hotel_port = form.cleaned_data.get("hotel_port")
            hotel_vpn_ip_address = form.cleaned_data.get("hotel_vpn_ip_address")
            hotel_vpn_port = form.cleaned_data.get("hotel_vpn_port")

            hotel_context = {"hotel_admin_id": hotel_admin_id,
                             "hotel_country": hotel_country,
                             "hotel_city": hotel_city,
                             "hotel_name": hotel_name,
                             "hotel_name_certification": hotel_name_certification,
                             "hotel_ip_address": hotel_ip_address,
                             "hotel_port": hotel_port,
                             "hotel_vpn_ip_address": hotel_vpn_ip_address,
                             "hotel_vpn_port": hotel_vpn_port,
                             }
            result = hotel_save.save_change_hotel(hotel_context)
            return JsonResponse({"result": result}, status=200)
        else:
            errors = hotel_save.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


'''delete hotel certificate from server and database'''


def delete_hotel(request):
    if request.is_ajax and request.method == "POST":
        form = Hotels_form(request.POST)
        hotel_add = Hotel_edit()
        if form.is_valid():
            hotel_name_certification = form.cleaned_data.get("hotel_name_certification")
            hotel_name_certification = hotel_name_certification.replace(' ', '')
            result = hotel_add.delete_hotel(hotel_name_certification)
            return JsonResponse({"result": result}, status=200)
        else:
            errors = hotel_add.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


''' create holte certificate in /etc/openvpn/clinet'''


def create_hotel_certificate(request):
    if request.is_ajax and request.method == "POST":
        form = Hotels_form(request.POST)
        cert_create = Hotel_edit()
        if form.is_valid():
            hotel_certification = form.cleaned_data.get("hotel_name_certification")
            hotel_certification = hotel_certification.replace(' ', '')
            data = cert_create.make_certificate(hotel_certification)
            return JsonResponse({"data": data}, status=200)
        else:
            errors = cert_create.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


'''get status of exist certificate'''


def get_status_cerificate(request):
    if request.is_ajax and request.method == "GET":
        check_certificate = Hotel_edit()
        hotel_certification = request.GET.get("hotel_name_certification")
        result = check_certificate.ckeck_status_cerificate(hotel_certification)
        return JsonResponse({"result": result}, status=200)


'''Copy certificate openvpn to remote host '''


def copy_certificate_to_host(request):
    if request.is_ajax and request.method == "POST":
        form_send_cert = Hotels_form(request.POST)
        send_cert = Hotel_edit()
        if form_send_cert.is_valid():
            login = form_send_cert.cleaned_data.get("login")
            password = form_send_cert.cleaned_data.get("password")
            ip = form_send_cert.cleaned_data.get("hotel_ip_address")
            port = form_send_cert.cleaned_data.get("hotel_port")
            hotel_name_certification = form_send_cert.cleaned_data.get("hotel_name_certification")
            hotel_name_certification = hotel_name_certification.replace(' ', '')
            result = send_cert.copy_cert_to_host(login, password, hotel_name_certification, ip, port)
            return JsonResponse({"result": result}, status=200)
        else:
            errors = send_cert.processing_form_errors(form_send_cert)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


def render_hotel_json(request):
    if request.is_ajax and request.method == "GET":
        json = Hotel_edit()
        hotel_json = json.get_hotel_json()
        return JsonResponse({"hotel_json": hotel_json}, status=200)


def create_vpn_server(request):
    return render(request, 'hotsrvpn/404.html')


