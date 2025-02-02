from restaurant.models import MenuItems 
from django.test import TestCase

class MenuItemsTest(TestCase):
    def test_get_item(self):
        item = MenuItems.objects.create(title="Icecream", price=2.00, inventory=3)
        self.assertEqual(item.title, "Icecream")
        self.assertEqual(item.price, 2.00)
        self.assertEqual(item.inventory, 3)
