
from django import template
register = template.Library()


censor_list = ['редиска', 'дурак', 'козел']

# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   for word in censor_list:
      value = value.replace(word[1:], '*' * len(word[1:]))

   return value

