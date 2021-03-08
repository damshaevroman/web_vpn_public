from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .configSerializer import ConfigSerializer
# Create your views here.
from deploy_client.forms import DataForm


@login_required(login_url='/')
def configserver(request):
    return render(request, 'configserver/configserver.html')

@api_view(['POST'])
def createServer(request):
    print('CREATE SERVER')
    data = request.data
    data = data.dict()
    print(data)
    print(request.FILES)
    serializer = ConfigSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        try:
            with open('/home/roman/Desktop/vpn_3.0/copy.conf', 'w') as file:
                file.write(str(request.FILES["crt"].read()) + str(request.FILES["cert"].read()) +
                           str(request.FILES["key"].read()) + str(request.FILES["dh"].read()) +
                           str(request.FILES["ta"].read()))
        except Exception as errors:
            print('THIS exception')
            print(errors)
            return Response(serializer.errors, status=400)

        return Response(status=200)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

