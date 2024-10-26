'''
# inventory/tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

class InventoryViewTests(APITestCase):
    
    def setUp(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(username='testuser', password='testpassword')
        
        # Obtain a JWT token for the created user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        print(self.access_token)

        # Set the inventory URL
        self.inventory_url = reverse('create_inventory')  # Adjust this to your URL pattern for inventory items
    
    def getItemURL(self, item_id):
        """Helper method to generate the inventory item URL dynamically."""
        return reverse('inventory_detail_update_delete', args=[item_id])
    
    def test_create_inventory_item(self):
        response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Item')
    
    def test_create_inventory_item(self):
        response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_create_existing_inventory_item(self):
        # Create the item first
        self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Try to create the same item again
        response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_inventory_item(self):
        # Create an inventory item
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        # Retrieve the inventory item
        response = self.client.get(self.getItemURL(item_id), 
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')  # Adjust the URL name if necessary
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_get_nonexistent_inventory_item(self):
        response = self.client.get(self.getItemURL(999),  # Assuming 999 does not exist
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_update_inventory_item(self):
        # Create an inventory item
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        # Update the inventory item
        response = self.client.put(self.getItemURL(item_id), {
            'name': 'Updated Test Item',
            'quantity': 20
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Item')
        self.assertEqual(response.data['quantity'], 20)
    
    def test_delete_inventory_item(self):
        # Create an inventory item
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        # Delete the inventory item
        response = self.client.delete(self.getItemURL(item_id),
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it has been deleted
        response = self.client.get(self.getItemURL(item_id),
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_nonexistent_inventory_item(self):
        response = self.client.delete(self.getItemURL(999),  # Assuming 999 does not exist
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

'''
# inventory/tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

class InventoryViewTests(APITestCase):
    
    def setUp(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(username='testuser', password='testpassword')
        
        # Obtain a JWT token for the created user
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Set the inventory URL
        self.inventory_url = reverse('create_inventory')  # Adjust this to your URL pattern for inventory items

    def getItemURL(self, item_id):
        """Helper method to generate the inventory item URL dynamically."""
        return reverse('inventory_detail_update_delete', args=[item_id])

    def test_create_inventory_item(self):
        response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Item')
        self.item_id = response.data['id']  # Store item ID for further tests

    def test_create_inventory_item_with_missing_fields(self):
        response = self.client.post(self.inventory_url, {
            'quantity': 10,  # Missing 'name'
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_existing_inventory_item(self):
        # Create the item first
        self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Try to create the same item again
        response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_get_inventory_item(self):
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        response = self.client.get(self.getItemURL(item_id), 
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_get_nonexistent_inventory_item(self):
        response = self.client.get(self.getItemURL(999),  
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_update_inventory_item(self):
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        response = self.client.put(self.getItemURL(item_id), {
            'name': 'Updated Test Item',
            'quantity': 20
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Item')
        self.assertEqual(response.data['quantity'], 20)

    def test_update_nonexistent_inventory_item(self):
        response = self.client.put(self.getItemURL(999), {
            'name': 'Updated Test Item',
            'quantity': 20
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_update_inventory_item_with_invalid_data(self):
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        # Attempt to set a negative quantity
        response = self.client.put(self.getItemURL(item_id), {
            'name': 'Updated Test Item',
            'quantity': -5  # Invalid data
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_inventory_item(self):
        item_response = self.client.post(self.inventory_url, {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for testing.',
            'price': 10
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        item_id = item_response.data['id']
        
        response = self.client.delete(self.getItemURL(item_id),
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.getItemURL(item_id),
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_inventory_item(self):
        response = self.client.delete(self.getItemURL(999),  
                                      HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_unauthorized_access(self):
        response = self.client.get(self.getItemURL(1))  # No auth header
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
