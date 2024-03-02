from datetime import datetime
import pytz
from django.db.models import Prefetch, Count
from learningapp.repositories import *

rep_user = UserRepository()
rep_group = GroupRepository()


def balance_groups(product: Product, user: User, min_count, max_count) -> None:
    """
    Функция, которая добавляет пользователя в группу если группы не заполнены
    или равномерно распределяет пользователей по группам
    :param product: объект класса Product
    :param user: Пользователь
    :param max_count: максимальное количество пользователей в группе
    :param min_count: минимальное количество пользователей в группе
    :return: None
    """
    groups = list(product.groups.all())
    groups.sort(key=lambda x: x.num_users)  # сортировка списка по кол-ву пользователей
    groups[0].users.add(user)
    groups[0].num_users += 1
    if all((groups[0].num_users >= min_count,
            groups[-1].num_users <= max_count,
            groups[-1].num_users - groups[0].num_users <= 1,
            )):  # если все условия соблюдены
        return
    else:  # равномерное распределение пользователей между группами:
        distribute_even(groups, max_count, min_count)


def distribute_even(groups: list[GroupLearn], max_count: int, min_count: int) -> None:
    """
    Функция, которая равномерно распределяет пользователей по группам
    с соблюдением условий максимального и минимального количества
    пользователей в учебной группе и разницей между количеством пользователей
    в каждой группе не более чем на 1
    :param groups: Список с объектами GroupLearn
    :param max_count: максимальное количество пользователей в группе
    :param min_count: минимальное количество пользователей в группе
    :return: None
    """
    diff = groups[-1].num_users - groups[0].num_users
    while diff > 1 or groups[-1].num_users > max_count:
        res_off = max_count - groups[-1].num_users
        if res_off < 0:  # если в группе пользователей больше max_count
            users_to_group_new = groups[-1].users[res_off:]  # лишние пользователи в группе
            groups.users.remove(*users_to_group_new)
            new_group = rep_group.save('group_learn_i', product, users_to_group_new)
            new_group.num_users = abs(res_off)
            groups.append(new_group)
        if diff > 1:  # если количество пользователей в группах различается больше чем на один
            user_to_move = groups[-1].users.first()
            groups[-1].users.remove(user_to_move)
            groups[0].users.add(user_to_move)
            groups[-1].num_users -= 1
            groups[0].num_users += 1
            diff = groups[-1].num_users - groups[0].num_users
        groups.sort(key=lambda x: x.num_users)


class AddUserProduct:
    """
    Класс для добавления пользователей
    в группу при получении доступа к продукту
    """

    @classmethod
    def add_to_group(cls, user_id: int, product_id: int) -> None:
        """
        Метод для добавления пользователя в группу
        при получении доступа к продукту
        :param user_id: идентификатор пользователя
        :param product_id: идентификатор продукта
        :return: None
        """
        groups_prefetch = Prefetch('groups',
                                   queryset=GroupLearn.objects.annotate(num_users=Count('users')))
        product = Product.objects.prefetch_related(groups_prefetch).get(pk=product_id)
        user = rep_user.get(user_id)
        max_count = product.max_count_users
        min_count = product.min_count_users
        if product.started_at > datetime.now().replace(tzinfo=pytz.utc):  # если продукт еще не начался
            balance_groups(product, user, min_count, max_count)
        else:
            groups_right = product.groups.filter(num_users__lt=max_count).order_by('-num_users')
            # группы, в которых количество участников меньше максимального числа
            if not groups_right:  # создать новую группу, если групп нет или все другие группы
                # заполнены
                rep_group.save('group_i', product, user)
            else:
                groups_right[0].users.add(user)
                # в группу с самым большим кол-вом участников добавляется пользователь,
                # по умолчанию группа заполняется до значения max_count
