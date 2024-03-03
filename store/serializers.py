from rest_framework import serializers
from .models import Product, Lesson, Group


class ProductListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'date_of_start', 'price', 'lesson_count']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(product=obj).count()
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    students_number = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_students_number(self, obj):
        return obj.students.count()
