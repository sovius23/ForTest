import datetime
from django.utils.deprecation import MiddlewareMixin

class SetLastVisitMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            request.user.last_seen = datetime.datetime.now()
            request.user.save()
        return response
