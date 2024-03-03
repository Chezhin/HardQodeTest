from django.urls import path
from .views import ProductListView, AvailableProductView, LessonListView, GroupListView


urlpatterns = [
    path('products-list/', ProductListView.as_view()),
    path('product/<int:pk>/', AvailableProductView.as_view()),
    path('lessons/<int:product_id>/', LessonListView.as_view()),
    path('groups/', GroupListView.as_view())
]
