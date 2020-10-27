from django.shortcuts import render
from django.http import JsonResponse

from dashboard.busineslogic.dashboard import Dashboard



'''render main dashboard'''
def dashboard(request):
    return render(request, 'dashboard.html')

''' back to front number of creates certifications of hotels and users'''
def counter_members_vpn_host(request):
    dashboard = Dashboard()
    count_context = dashboard.vpnCounter()
    return JsonResponse({"count_context": count_context }, status=200)

'''back to front information abnout system resourse CPU and memory'''
def server_status(request):
    dashboard = Dashboard()
    server_status, cpu2 = dashboard.server_status()
    return JsonResponse({"server_status": server_status, "cpu2": cpu2}, status=200)


'''enable method which check via fping host '''
def ping_hosts(request):
        dashboard = Dashboard()
        count_context = dashboard.vpnCounter()
        return JsonResponse({"count_context": count_context}, status=200)

'''This method get records from database Hotel which dont have vpn ip address and records which unavailible via vpn
 address (use fping for check availble) and send to front 2 arrays'''
def check_non_ip_host(request):
    dashboard = Dashboard()
    count_context, list_unavailible_host = dashboard.non_ip_host()
    return JsonResponse({"count_context": count_context, "list_unavailible_host": list_unavailible_host}, status=200)








# @api_view(['GET'])
# def apiOverview(request):
#     dashboart_url = {
#         'ping': '/check_non_ip_host/',
#         'List': '/check_non_pinged_host/',
#     }
#     return Response(dashboart_url)

# @api_view(['GET'])
# def check_non_ip_host(request):
#     non_ip_host =
#     count_hotel = Hotel.objects.all()
#     serializer = IPvpnSerializer(count_hotel, many=True)
#     return Response(serializer.data)
#
#
#
#
#
# @api_view(['GET'])
# def taskList(request):
#     dashboard = Dashboard()
#     data = dashboard.vpnCounter()
#     return JsonResponse({"data": data}, status=200)
#     # count_hotel = Hotel.objects.all()
#     # serializer = HotelSerializer(count_hotel, many=True)
#     # return Response(serializer.data)
#
#
# @api_view(['GET'])
# def taskDetail(request, pk):
#     tasks = Task.objects.get(id=pk)
#     print('THIS TASK')
#     print(tasks)
#     serializer = TaskSerializer(tasks, many=False)
#     print('THIS SERIALIZE TASK')
#     print(serializer)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def taskCreate(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response('save')
#
# @api_view(['POST'])
# def taskUpdate(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
#
# @api_view(['DELETE'])
# def taskDelete(request, pk):
#     task = Task.objects.get(id=pk)
#     task.delete()
#     return Response('DELETED')
#
