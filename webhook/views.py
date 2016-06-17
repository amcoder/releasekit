from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def webhook(request, queue=None):
    event = request.META.get('HTTP_X_GITHUB_EVENT')
    try:
        data = json.loads(request.body) if request.body else {}
    except ValueError as e:
        return HttpResponseBadRequest("Invalid json body")

    queue(event, data)

    return JsonResponse({ 'event': event })
