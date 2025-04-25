from django import template
from django.db.models import Count, Q
from django.core.cache import cache

from cooking.models import Category


register = template.Library()


# @register.simple_tag()
# def get_all_categories():
#     """Кнопки категорий"""
#     return Category.objects.annotate(cnt=Count("posts")).filter(
#         Q(cnt__gt=0) & Q(posts__is_published=True),
#     )

# Кэширование на низкоуровневом API
@register.simple_tag()
def get_all_categories():
    """Кнопки категорий"""
    buttons = cache.get("category")

    if not buttons:
        buttons = Category.objects.annotate(cnt=Count("posts")).filter(
            Q(cnt__gt=0) & Q(posts__is_published=True),
        )
        cache.set("category", buttons, 60)
    
    return buttons

