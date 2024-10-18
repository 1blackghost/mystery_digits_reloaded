# your_app/middleware.py

from django.http import HttpResponseForbidden
import re

class MobileOnlyMiddleware:
    MOBILE_USER_AGENT_RE = re.compile(r'.*(iphone|ipod|android|blackberry|iemobile|mobile).*', re.IGNORECASE)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.is_mobile(request.META.get('HTTP_USER_AGENT', '')):
            return HttpResponseForbidden("This page is only accessible on mobile devices.")
        return self.get_response(request)

    @classmethod
    def is_mobile(cls, user_agent):
        return bool(cls.MOBILE_USER_AGENT_RE.match(user_agent))
