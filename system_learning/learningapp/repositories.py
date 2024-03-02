from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from learningapp.models import *
from typing import Union


class UserRepository:
    model = User

    def get(self, user_id: int) -> User:
        return self.model.objects.get(pk=user_id)


class ProductRepository:
    model = Product

    def get_list(self) -> QuerySet[Product]:
        return self.model.objects.all()

    def get(self, product_id: int) -> Product:
        return get_object_or_404(self.model, pk=product_id)


class GroupRepository:
    model = GroupLearn

    def save(self, name: str, product: Product, users: Union[list[User], User]) -> GroupLearn:
        inst = self.model.objects.create(name=name,
                                         product=product,
                                         users=users if isinstance(users, list) else [users])
        return inst


class LessonsRepository:
    model = Lesson

    def get_by_product(self, product: Product) -> QuerySet[Lesson]:
        return self.model.objects.filter(product=product)
