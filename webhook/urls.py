from django.conf.urls import url
from . import views

def queue(event, data):
    print("Queuing event: %s, data: %s" % (event, data))

urlpatterns = [
    url(r'^/?$', views.webhook, {'queue': queue}, name='webhook'),
]
