from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ItemSerializer
from rest_framework import status

from core.models import Item


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
		'List': '/api/list//',
		'Detail': '/api/detail/{pk}/',
		'New': '/api/create/',
		'Update': '/api/update/{pk}/',
		'Delete': '/api/delete/{pk}/',
	}
    return Response(api_urls)

@api_view(['GET'])
def itemsList(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def itemDetail(request, pk):
    item = Item.objects.get(pk=pk)
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def itemCreate(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("Serializer is valid")
    else:
        print("Serializer is not valid:", serializer.errors)
    return Response(serializer.data)

@api_view(['POST'])
def itemUpdate(request, pk):
    item = Item.objects.get(pk=pk)
    serializer = ItemSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def itemDelete(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)