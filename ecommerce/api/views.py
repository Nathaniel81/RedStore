"""
Module: core.api.views

This module contains API views for interacting with item data.

API views:
- apiOverview: Provides an overview of available API endpoints.
- itemsList: Retrieves a list of all items.
- itemDetail: Retrieves details of a specific item by ID.
- itemCreate: Creates a new item.
- itemUpdate: Updates an existing item.
- itemDelete: Deletes an item by ID.

Each API view is documented with its purpose and usage.
"""

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ItemSerializer
from rest_framework import status, permissions

from core.models import Item

@api_view(['GET'])
def apiOverview(request):
    """
    API Overview View

    Provides an overview of available API endpoints.

    Usage:
    - GET: Returns a dictionary of available API endpoints.
    """

    api_urls = {
        'List': '/api/list/',
        'Detail': '/api/detail/{pk}/',
        'New': '/api/create/',
        'Update': '/api/update/{pk}/',
        'Delete': '/api/delete/{pk}/',
    }

    return Response(api_urls)

@api_view(['GET'])
def itemsList(request):
    """
    Items List View

    Retrieves a list of all items.

    Usage:
    - GET: Returns a serialized list of all items.
    """

    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def itemDetail(request, pk):
    """
    Item Detail View

    Retrieves details of a specific item by ID.

    Usage:
    - GET: Returns a serialized item based on the provided ID.
    """

    item = Item.objects.get(pk=pk)
    serializer = ItemSerializer(item, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def itemCreate(request):
    """
    Item Create View

    Creates a new item.

    Usage:
    - POST: Creates a new item with the provided data.
    """

    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def itemUpdate(request, pk):
    """
    Item Update View

    Updates an existing item.

    Usage:
    - POST: Updates an existing item with the provided data.
    """

    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def itemDelete(request, pk):
    """
    Item Delete View

    Deletes an item by ID.

    Usage:
    - DELETE: Deletes an item based on the provided ID.
    """

    try:
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
