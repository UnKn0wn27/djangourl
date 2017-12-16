from django.conf.urls import url
from .views import wildcar_redirect

urlpatterns = [
    url(r'^(?P<path>.*)', wildcar_redirect),
]
