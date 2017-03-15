from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class IpFilter(MiddlewareMixin):

    def process_request(self, request):
        if request.environ['REMOTE_ADDR'] == '192.168.0.104':
            return HttpResponse('Your request has been rejected...')

    def process_response(self, request, response):
        return response