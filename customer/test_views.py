from django.test import TestCase
from django.urls import reverse

class TestMenusViews(TestCase):
    def setUp(self):
        self.menu_url = reverse('menu')
        self.order_url = reverse('order')
        self.order_confirmation_url = reverse('order_confirmation')

    def test_menu_GET(self):
        response = self.client.get(self.menu_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/menu.html')

    def test_order_GET(self):
        response = self.client.get(self.order_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/order.html')
