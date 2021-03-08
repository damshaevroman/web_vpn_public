from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .businesslogic.serializer import UserSerializer
from .forms import Hotel_User_form
from hotsrvpn.businesslogic.user_edit import User_edit
from django.http import JsonResponse
from django.http import FileResponse


@login_required(login_url='/')
def render_user_main_page(request):
    user_form = Hotel_User_form()
    user_json = User_edit()
    users_json = user_json.get_database()
    return render(request, 'hotsrvpn/user/user_vpn_table.html', {"user_form": user_form, "json_users": users_json})


def render_user_json(request):
    if request.is_ajax and request.method == "GET":
        user_json = User_edit()
        user_json = user_json.get_database()
        return JsonResponse({"user_json": user_json}, status=200)

@api_view(['POST'])
def create_user(request):
    """Get data from Form and add to database table Hotel_user"""
    if request.method == "POST":
        hotelSerialize = UserSerializer(data=request.data)
        if hotelSerialize.is_valid():
            userData = User_edit()
            user_json = userData.write_user_to_database(hotelSerialize)
            return Response(user_json.data, status=200)
        return Response(hotelSerialize.errors, status=400)



@login_required(login_url='/')
def show_edit_user_page(request, id):
    status_certificate = User_edit()
    user_form = Hotel_User_form()
    user, check_certeficate_status = status_certificate.edit_user_page(id)
    return render(request, "hotsrvpn/user/edit_user.html",
                  {"user": user, "user_form": user_form, "check_certeficate_status": check_certeficate_status})


def save_edit_user_form(request):
    """ get information from HTML page edti_user (form -  save_edit_user_form) change and save infortation to
    database table Hotel_User """
    if request.is_ajax and request.method == "POST":
        form = Hotel_User_form(request.POST)
        user_add = User_edit()
        if form.is_valid():
            organization = form.cleaned_data.get("organization")
            user_city = form.cleaned_data.get("user_city")
            user_fio = form.cleaned_data.get("user_fio")
            user_cert = form.cleaned_data.get("user_cert")
            user_cert = user_cert.replace(' ', '')
            result = user_add.save_change_user(organization, user_city, user_fio, user_cert)
            return JsonResponse({"result": result}, status=200)
        else:
            errors = user_add.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


def delete_user(request):
    """Delete user certificate from database and server"""
    if request.is_ajax and request.method == "POST":
        form = Hotel_User_form(request.POST)
        user_add = User_edit()
        if form.is_valid():
            user_cert = form.cleaned_data.get("user_cert")
            user_cert = user_cert.replace(' ', '')
            result = user_add.delete_user(user_cert)
            return JsonResponse({"result": result}, status=200)
        else:
            errors = user_add.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


def create_user_certificate(request):
    """ create certificate"""
    if request.is_ajax and request.method == "POST":
        form = Hotel_User_form(request.POST)
        user_add = User_edit()
        if form.is_valid():
            user_cert = form.cleaned_data.get("user_cert")
            user_cert = user_cert.replace(' ', '')
            data = user_add.make_certificate(user_cert)
            return JsonResponse({"data": data}, status=200)
        else:
            errors = user_add.processing_form_errors(form)
            return JsonResponse({"error": errors}, status=430)
    return JsonResponse({"error": "не могу покдлючится проверьте данные"}, status=450)


def ckeck_status_cerificate(request):
    if request.is_ajax and request.method == "GET":
        check_certificate = User_edit()
        result = check_certificate.ckeck_status_cerificate()
        return JsonResponse({"result": result}, status=200)

@api_view(['GET'])
def render_user_json(request):
    if request.is_ajax and request.method == "GET":
        json = User_edit()
        user_json = json.get_user_json()
        return Response(user_json.data, status=200)


@api_view(['POST'])
def send_user_file_front(request):
    """This method send file certificate to browser"""
    if request.is_ajax and request.method == "POST":
        data = request.data.dict()
        data = data["user_cert"]
        file = open(f'/etc/openvpn/client/{data}/{data}.conf', 'rb')
        response = FileResponse(file.read().decode('utf8'))
        return response
