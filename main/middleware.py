# your_app/middleware.py

from django.http import HttpResponse
from django.conf import settings
import os

class MobileOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.is_mobile(request.META.get('HTTP_USER_AGENT', '')):
            return self.serve_image()
        return self.get_response(request)

    def is_mobile(self, user_agent):
        return any(keyword in user_agent.lower() for keyword in ['iphone', 'ipod', 'android', 'blackberry', 'iemobile', 'mobile'])

    def serve_image(self):
        image_path = os.path.join(settings.BASE_DIR, 'main','static', 'images', 'desktop.jpg')
        with open(image_path, 'rb') as image_file:
            return HttpResponse(image_file.read(), content_type='image/jpeg')
