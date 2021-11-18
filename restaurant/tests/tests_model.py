from django.test import TestCase

from ..models import Restaurant


class RestaurantTest(TestCase):
    def setUp(self) -> None:
        Restaurant.objects.create(
            name='Restaurant 1', address='A Street. No: 6', phone='+48123456789'
        )
        Restaurant.objects.create(
            name='Restaurant 2', address='B Street. No: 2', phone='+48987654321'
        )
