
import pizza


def greet_user(first_name, second_name):
    name = {'first name': first_name, 'second name': second_name}
    return name


pizza.make_pizza(12, 'haha', 'heheh')
name = greet_user('fang', 'wentao')
print(name)
