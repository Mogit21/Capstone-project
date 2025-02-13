from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Menu  # Assuming the Menu model is in the same app
from .serializers import MenuSerializer  # Assuming you have a MenuSerializer for serialization

#TODO to understand the code !!!!!!!!!!!!!!


class MenuViewTest(TestCase):

    def setUp(self):
        """
        Set up test instances of Menu model for the tests
        """
        # Create test instances of the Menu model
        self.menu_item_1 = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.menu_item_2 = Menu.objects.create(title="Burger", price=50, inventory=150)
        self.menu_item_3 = Menu.objects.create(title="Pizza", price=120, inventory=80)

        # Instantiate the test client to simulate API requests
        self.client = APIClient()

    def test_getall(self):
        """
        Test to retrieve all Menu objects and check serialized data
        """
        # Make a GET request to retrieve all Menu items
        response = self.client.get('/api/menu/')  # Adjust the URL based on your URL patterns

        # Serialize the data
        menu_items = Menu.objects.all()  # Get all Menu objects
        serialized_data = MenuSerializer(menu_items, many=True).data  # Serialize the data

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the response status is OK
        self.assertEqual(response.data, serialized_data)  # Check if the serialized data matches the response data
