from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Inventory
from .InventorySerializer import InventorySerializer
import logging
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class InventoryView(APIView):
    permission_classes = [IsAuthenticated]

    # POST: Create a new inventory item
    def post(self, request):
        logger.info(f"Received request to create inventory item with data: {request.data}")
        
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Inventory item created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Failed to create inventory item. Errors: {serializer.errors}")
        return Response({'error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        logger.info(f"Received request to retrieve inventory item with ID: {id}")
        
        # Check if the item is in the cache
        cached_item = cache.get(f'inventory_item_{id}')
        if cached_item:
            logger.info("Cache hit: Returning cached data.")
            return Response(cached_item, status=status.HTTP_200_OK)

        try:
            item = Inventory.objects.get(id=id)
            serializer = InventorySerializer(item)
            cache.set(f'inventory_item_{id}', serializer.data, timeout=3600)  # Cache for 1 hour
            logger.info("Inventory item retrieved successfully from the database.")
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist: Inventory item with ID {id} not found. Error: {str(e)}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT: Update an existing inventory item by ID
    def put(self, request, id):
        logger.info(f"Received request to update inventory item with ID: {id} and data: {request.data}")
        
        try:
            item = Inventory.objects.get(id=id)
            serializer = InventorySerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info("Inventory item updated successfully.")
                return Response(serializer.data)
            logger.warning(f"Failed to update inventory item. Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist: Inventory item with ID {id} not found for update. Error: {str(e)}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: Delete an inventory item by ID
    def delete(self, request, id):
        logger.info(f"Received request to delete inventory item with ID: {id}")
        
        try:
            item = Inventory.objects.get(id=id)
            item.delete()
            logger.info("Inventory item deleted successfully.")
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            logger.error(f"ObjectDoesNotExist: Inventory item with ID {id} not found for deletion. Error: {e}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    