from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Menu  # Assuming the Menu model is in the same app
from restaurant.serializers import MenuSerializer  # Assuming you have a MenuSerializer for serialization


#TODO Check the errors when rnning the tests below

class MenuViewTest(TestCase):
    def setUp(self):
        """Create test instances of the Menu model"""
        self.client = APIClient()
        self.item1 = Menu.objects.create(title="Burger", price=5.99, inventory=10)
        self.item2 = Menu.objects.create(title="Pizza", price=8.99, inventory=20)
        self.item3 = Menu.objects.create(title="Pasta", price=7.49, inventory=15)
        self.valid_payload = {"title": "Salad", "price": 4.99, "inventory": 30}
        self.invalid_payload = {"title": "", "price": -1, "inventory": -5}

    def test_get_all_menus(self):
        """Test retrieving all menu items via API"""
        response = self.client.get("/restaurant/menu/")
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_create_menu_valid(self):
        """Test creating a new menu item with valid data"""
        response = self.client.post("/restaurant/menu/", data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 4)  # Three initial + one new

    def test_create_menu_invalid(self):
        """Test creating a menu item with invalid data"""
        response = self.client.post("/restaurant/menu/", data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_menu(self):
        """Test updating an existing menu item"""
        update_data = {"title": "Vegan Pizza", "price": 10.99, "inventory": 25}
        response = self.client.put(f"/restarant/menu/{self.item2.id}/", data=update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item2.refresh_from_db()
        self.assertEqual(self.item2.title, "Vegan Pizza")
        self.assertEqual(self.item2.price, 10.99)
        self.assertEqual(self.item2.inventory, 25)

    def test_delete_menu(self):
        """Test deleting a menu item"""
        response = self.client.delete(f"/restarant/menu/{self.item1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 2)  # One less after deletion
