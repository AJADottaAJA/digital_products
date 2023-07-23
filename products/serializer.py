from rest_framework import serializers
from .models import Category, File, Product


class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = ["id", "title", "file", "file_type"]

    def get_file_type(self, obj):
        return obj.get_file_type_display()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title", "description", "avatar")

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # agar faqat az een "serializers.ModelSerializer" ers bebari nemitooni link be post detail bezani
    categories = CategorySerializer(many=True)
    files = FileSerializer(many=True)
    x = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "title", "description", "avatar", "categories", "files", "x", "url"]
        #fields = ["title", "description", "avatar", "categories", "file_set", "x"]         # vali bayad related_name ro dar file "model" pak koni

    def get_x(self, obj):
        return ["ali", "reza", "mobina"], [1, 2]