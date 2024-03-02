from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import LessonSerializer, ProductSerializer
from learningapp.repositories import *

rep_prod = ProductRepository()
rep_lesson = LessonsRepository()


class ProductApiView(generics.ListAPIView):
    queryset = rep_prod.get_list()
    serializer_class = ProductSerializer


class LessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = rep_prod.get(product_id)
        if not product.access_user(request.user.id):
            return Response({"error": "У вас нет доступа к этому продукту"}, status=status.HTTP_403_FORBIDDEN)

        lessons = rep_lesson.get_by_product(product)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
