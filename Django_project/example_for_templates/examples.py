# from jinja2 import Template
#
# class Person():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
# per = Person('Федор', 23)
#
# tm = Template("Мне {{ p.age }} лет и зовут меня {{ p.name }}")
# msg = tm.render(p = per)
#
#
# # name = 'Федор'
# # age = 28
# #
# # # Создаем экземпляр класс Template
# # tm = Template("Мне {{ a }} лет и зовут меня {{ n }}.")
# # msg = tm.render(n = name, a = age)
# #
# # print(msg)
#
# # {%%} - спецификатор шаблона
# # {{}} - выражение для вставки конструкций Python в шаблон
# # {##} - блок комментариев
#
#
#
#
# # Способы экранирования
#
# data = 'sasdfd {{ name }}'
#
# tp = Template(data)
# mes = tp.render(name = 'кто-то')
#
#
#
#
# # {%%} - спецификатор шаблона
# data_2 = '{% raw %} asdasd {{name}} asdas {% endraw %}'
#
# tp_2 = Template(data_2)
# mes_2 = tp_2.render(name = 'кто-то')
#
#
#
# # Экранирование производится таких символов, какие браузер воспринимает как теги
#
# link = '''В HTML-документе ссылки определяются так:
# <a href="#">Ссылка</a>'''
#
# tm = Template("{{ link | e}}")
# msg = tm.render(link=link)
#
# # Блок for
#
# cities = [{'id': 1, 'city': 'Москва'},
#           {'id': 5, 'city': 'Тверь'},
#           {'id': 7, 'city': 'Минск'},
#           {'id': 8, 'city': 'Смоленск'},
#           {'id': 11, 'city': 'Калуга'}]
#
# # option - это не какой-то специальный тэг, что просто текст
# # знак минус убирает перенос строки
# link = '''<select name="cities">
# {% for c in cities -%}
#     <option value="{{c['id']}}">{{c['city']}}</option>
# {% endfor -%}
# </select>'''
#
# tm = Template(link)
# msg = tm.render(cities=cities)
#
# # Блок if
#
# cities = [{'id': 1, 'city': 'Москва'},
#           {'id': 5, 'city': 'Тверь'},
#           {'id': 7, 'city': 'Минск'},
#           {'id': 8, 'city': 'Смоленск'},
#           {'id': 11, 'city': 'Калуга'}]
#
# # option - это не какой-то специальный тэг, что просто текст
# # знак минус убирает перенос строки
# link = '''<select name="cities">
# {% for c in cities -%}
# {% if c.id > 6 -%}
#     <option value="{{c['id']}}">{{c['city']}}</option>
# {% elif c.city == "Москва" -%}
#     <option>{{c.city}}</option>
# {% else -%}
#     {{c.city}}
# {% endif -%}
# {% endfor -%}
# </select>'''
#
# tm = Template(link)
# msg = tm.render(cities=cities)
#
#
#
# # Фильтры
# cars = [
#     {'model': 'Ауди', 'price': 23000},
#     {'model': 'Шкода', 'price': 17300},
#     {'model': 'Вольво', 'price': 44300},
#     {'model': 'Фольксваген', 'price': 21300}
# ]
# # cs - для какой коллекции будет вызываться фильтр
# # sum - фильтр, суммирование по атрибуту (attribute) price
# # синтаксис фильтра sum(iterable, attribute, start=0)
# tpl = "Суммарная цена автомобилей {{ cs | sum(attribute='price') }}"
# tm = Template(tpl)
# msg = tm.render(cs = cars)
# print(msg)
#
# # Блок filter
#
# persons = [
#     {"name": "Алексей", "old": 18, "weight": 78.5},
#     {"name": "Николай", "old": 28, "weight": 82.3},
#     {"name": "Иван", "old": 33, "weight": 94.0}
# ]
#
# tpl = '''
# {%- for u in users -%}
# {% filter upper %}{{u.name}}{% endfilter %}
# {% endfor %}
# '''
#
# tm = Template(tpl)
# mas = tm.render(users=persons)
#
# print(mas)
#
# # Макроопределения
#
# # Определяем шаблон поля ввода, а затем определяем три поля ввода
# html = '''
# {% macro input(name, value='', type='text', size=20) -%}
#     <input type="{{ type }}" name="{{ name }}" value="{{ value|e }}" size="{{ size }}">
# {%- endmacro %}
#
#
# {{ input('username') }}
# {{ input('email') }}
# {{ input('password') }}
# '''
#
# # Call
#
# persons = [
#     {"name": "Алексей", "old": 18, "weight": 78.5},
#     {"name": "Николай", "old": 28, "weight": 82.3},
#     {"name": "Иван", "old": 33, "weight": 94.0}
# ]
#
# html = '''
# {% macro list_users(list_of_users) -%}
# <ul>
# {% for u in list_of_users -%}
#     <li>{{u.name}}
# {%- endfor %}
# </ul>
# {%- endmacro %}
#
# {{list_users(users)}}
# '''
#
# tmp = Template(html)
# msg = tmp.render(users=persons)
#
#
# html = '''
# {% macro list_users(list_of_user) -%}
# <ul>
# {% for u in list_of_user -%}
#     <li>{{u.name}} {{caller(u)}}
# {%- endfor %}
# </ul>
# {%- endmacro %}
#
# {% call(user) list_users(users) %}
#     <ul>
#     <li>age: {{user.old}}
#     <li>weight: {{user.weight}}
#     </ul>
# {% endcall -%}
# '''
#
# tmp = Template(html)
# msg = tmp.render(users=persons)
#
#
# # Загрузчики шаблонов
#
# from jinja2 import Environment, FileSystemLoader
# persons = [
#     {"name": "Алексей", "old": 18, "weight": 78.5},
#     {"name": "Николай", "old": 28, "weight": 82.3},
#     {"name": "Иван", "old": 33, "weight": 94.0}
# ]
#
# # загружвем шаблон
# file_loader = FileSystemLoader("")
# env = Environment(loader=file_loader)
#
# tm = env.get_template('page.htm') # Формирует Template на основе содержимого main.htm
# msg = tm.render(users = persons)
#
#
# # Конструкции include и import
# # Приммер в файле page.htm
#
# file_loader = FileSystemLoader("")
# env = Environment(loader=file_loader)
#
# tm = env.get_template("page.htm")
# msg = tm.render(domain="fdsf", title="something")
#
#
#
# # Наследование и расширение шаблона
#
# file_loader = FileSystemLoader('')
# env = Environment(loader=file_loader)
#
# template = env.get_template('about.htm')
#
# output = template.render()
# print(output)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
