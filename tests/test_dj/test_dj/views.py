from django.http import HttpResponse

from src.sdk.send_msg import AliyunSendMSG


def simple_view(request):
    c = AliyunSendMSG('tengxunyun')
    return HttpResponse("Hello, this is a simple response!")
