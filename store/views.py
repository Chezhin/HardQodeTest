from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Product, Lesson, Group
from rest_framework.permissions import AllowAny
from .serializers import ProductListSerializer, ProductSerializer, LessonSerializer, GroupSerializer
from .services import adding_student_to_group
from .permissions import HavingAccess


class ProductListView(generics.ListAPIView):
    '''
    Предоставляет список продуктов с основной информацией
    и количеством уроков.
    '''
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)


class AvailableProductView(generics.RetrieveAPIView):
    '''
    При наличии доступа к продукту определяет юзера в группу и
    предоставляет более подробную информацию. 
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_access(self, instance, serializer, user):
        if not user.is_authenticated:
            return Response({"error": "Пользователь не аутентифицирован"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if instance.author == user or Group.objects.filter(product=instance, students=user).exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if adding_student_to_group(instance, user) is None:
            return Response({"message": "Мест в группах не осталось"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.check_access(instance, serializer, request.user)
        




class LessonListView(generics.ListAPIView):
    '''
    Список уроков по продукту, к которому юзер имеет доступ.
    '''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, HavingAccess]

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        lessons = self.queryset.filter(product_id=product_id)
        return Response(self.serializer_class(lessons, many=True).data, status=status.HTTP_200_OK)
    

class GroupListView(generics.ListAPIView):
    '''
    Предоставляет список всех групп с количеством 
    участников.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
