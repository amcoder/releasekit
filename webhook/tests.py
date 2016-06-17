from django.test import TestCase, RequestFactory
from mock import Mock
from .views import webhook
import json

class WebhookTestCase(TestCase):
    def setUp(self):
        self.queue = Mock()
        self.request = RequestFactory().post( '/',
                '{"foo": "bar"}',
                HTTP_X_GITHUB_EVENT='some event',
                content_type='application/json',
                )

    def test_webhook_response(self):
        """Webhook returns correct response"""
        response = webhook(self.request, queue=self.queue)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['event'], 'some event')

    def test_webhook_queues_job(self):
        """Webhook queues job"""
        webhook(self.request, queue=self.queue)

        self.queue.assert_called_with('some event', { 'foo': 'bar' })

    def test_webhook_bad_json(self):
        """Webhook queues job"""
        request = RequestFactory().post( '/',
                'invalid json',
                HTTP_X_GITHUB_EVENT='some event',
                content_type='application/json',
                )
        response = webhook(request, queue=self.queue)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Invalid json body")
