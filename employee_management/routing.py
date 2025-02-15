from django.urls import re_path
from .consumers import EmployeeConsumer, LoginConsumer

websocket_urlpatterns = [
    re_path(r"ws/employees/$", EmployeeConsumer.as_asgi()),
    re_path(r'ws/login_updates/$', LoginConsumer.as_asgi()),
]



# daphne core.asgi:application    