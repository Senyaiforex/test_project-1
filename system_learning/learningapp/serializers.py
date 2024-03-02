from rest_framework import serializers
from .models import Product, Lesson
from django.db.models import Count, Avg
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()
    fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('author', 'name', 'started_at', 'price', 'lessons_count',
                  'users_count', 'fill_percentage', 'purchase_percentage')

    def get_users_count(self, obj):
        """
        Количество пользователей, занимающихся на продукте
        :param obj:
        :return:
        """
        return obj.groups.all().aggregate(total_users=Count('users'))['total_users']

    def get_lessons_count(self, obj):
        """
        Количество уроков в продукте
        :param obj:
        :return:
        """
        return Lesson.objects.filter(product=obj).count()

    def get_fill_percentage(self, obj):
        """
        Заполненность групп
        :param obj:
        :return:
        """
        max_users_count = obj.max_count_users
        avg_users_per_group = obj.groups.annotate(users_count=Count('users')).aggregate(
            avg_users=Avg('users_count')
        )['avg_users'] or 0

        fill_percentage = (avg_users_per_group / max_users_count) * 100
        return round(fill_percentage, 2)

    def get_purchase_percentage(self, obj):
        """
        Процент приобретения продукта
        :param obj:
        :return:
        """
        accessible_users_count = User.objects.filter(groups_learn__product=obj).distinct().count()
        total_users_count = User.objects.all().count()
        if total_users_count == 0:
            return 0  # Предотвращение деления на ноль

        purchase_percentage = (accessible_users_count / total_users_count) * 100
        return round(purchase_percentage, 2)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'link_video']
