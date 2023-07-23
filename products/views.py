from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, Category, File

from .serializer import ProductSerializer, CategorySerializer, FileSerializer



# Create your views here.


class ProductListView(APIView):
    # baraye ejad mahdoodiat een ke har kasi natoone list product haro bebine
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # baraye een ke bebinim kodoom user dare een URL ro search mikone
        print(request.user)
        print(request.auth)


        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={"request":request})
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            pro = Product.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser_pro = ProductSerializer(pro, context={"request":request})
        return Response(ser_pro.data)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        ser_cat = CategorySerializer(categories, many=True, context={"request":request})
        return Response(ser_cat.data)

class CategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            catogory = Category.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            ser_cat = CategorySerializer(catogory, context={"request":request})
            return Response(ser_cat.data)

class FileListView(APIView):
    def get(self, request, product_pk):
        files = File.objects.filter(product_id=product_pk)
        ser_files = FileSerializer(files, many=True, context={"request":request})
        return Response(ser_files.data)

class FileDetailView(APIView):
    def get(self, request, product_pk, pk):
        try:
            file = File.objects.get(product_id=product_pk, pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            ser_file = FileSerializer(file, context={"request":request})
            return Response(ser_file.data)