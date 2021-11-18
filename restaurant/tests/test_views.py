import json

from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Restaurant
from ..serializers import RestaurantSerializer

client = Client()


class RestaurantTestBase(TestCase):
    def setUp(self) -> None:
        self.restaurant1: Restaurant = Restaurant.objects.create(
            name='Restaurant 1', address='A Street. No: 1', phone='+48123456789'
        )
        self.restaurant2: Restaurant = Restaurant.objects.create(
            name='Restaurant 2', address='B Street. No: 2', phone='+48987654321'
        )
        self.restaurant3: Restaurant = Restaurant.objects.create(
            name='Restaurant 3', address='C Street. No: 3', phone='+48345678912'
        )
        self.restaurant4: Restaurant = Restaurant.objects.create(
            name='Restaurant 4', address='D Street. No: 4', phone='+48765432198'
        )
        self.url_list_create = reverse('restaurants:restaurant-list-create')

    @staticmethod
    def url_retrieve_update_delete(pk: int):
        return reverse('restaurants:restaurant-retrieve-update-delete', kwargs={'pk': pk})


class ListRestaurantsTest(RestaurantTestBase):
    def test_get_all_restaurants(self):
        resp = client.get(self.url_list_create)

        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class CreteRestaurantTest(RestaurantTestBase):
    def setUp(self) -> None:
        super(CreteRestaurantTest, self).setUp()

        self.valid_req_body = {
            'name': 'New Restaurant',
            'address': "new restaurant's address",
            'phone': '+48111111111',
        }

        self.invalid_req_body = {
            'address': "new restaurant's address",
            'phone': '+48111111111',
        }

    def test_successful_create_restaurant(self):
        resp = client.post(
            self.url_list_create,
            data=json.dumps(self.valid_req_body),
            content_type='application/json',
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_failed_create_restaurant(self):
        resp = client.post(
            self.url_list_create,
            data=json.dumps(self.invalid_req_body),
            content_type='application/json',
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveSingleRestaurantTest(RestaurantTestBase):
    def test_get_valid_single_restaurant(self):
        r_exist = self.restaurant2
        resp = client.get(self.url_retrieve_update_delete(r_exist.pk))

        restaurant = Restaurant.objects.get(pk=r_exist.pk)
        serializer = RestaurantSerializer(restaurant)

        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_restaurant(self):
        resp = client.get(self.url_retrieve_update_delete(9999))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class UpdateRestaurantTest(RestaurantTestBase):
    def setUp(self) -> None:
        super(UpdateRestaurantTest, self).setUp()

        self.valid_payload = {
            'name': 'Restaurant renamed',
            'address': self.restaurant3.address,
            'phone': self.restaurant3.phone,
        }

        self.invalid_payload = {}

    def test_successful_update_restaurant(self):
        resp = client.put(
            self.url_retrieve_update_delete(self.restaurant3.pk),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_not_found_update_restaurant(self):
        resp = client.put(
            self.url_retrieve_update_delete(9999),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_update_restaurant(self):
        resp = client.put(
            self.url_retrieve_update_delete(self.restaurant3.pk),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRestaurantTest(RestaurantTestBase):
    def test_successful_delete_restaurant(self):
        resp = client.delete(self.url_retrieve_update_delete(self.restaurant4.pk))

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_found_delete_restaurant(self):
        resp = client.delete(self.url_retrieve_update_delete(9999))

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
