"""Самое простое фласк-приложение на реакцию GET и POST Запросов."""

from flask import request, Flask, jsonify
from playhouse.shortcuts import model_to_dict
from data_model import Drivers, Clients, Orders

app = Flask(__name__)
state = ('not_accepted', 'in_progress', 'done', 'cancelled')


@app.route('/drivers', methods=['POST'])
def add_driver() -> str:
    """Добавить водителя."""
    js = request.get_json()
    Drivers.create(name=js.get('name'), car=js.get('car'))
    return 'Driver create'


@app.route('/drivers', methods=['GET'])
def search_driver() -> object:
    """Найти водителя."""
    pr = request.args.get('driverId')
    query = Drivers.get_by_id(pr)
    json_data = jsonify(model_to_dict(query))
    return json_data


@app.route('/drivers', methods=['DELETE'])
def del_driver() -> str:
    """Удалить водителя."""
    pr = request.args.get('driverId')
    res = Drivers.delete_by_id(pr)
    return f'Удален {res} водитель'


@app.route('/clients', methods=['POST'])
def add_clients() -> str:
    """Добавить клиента."""
    js = request.get_json()
    Clients.create(name=js.get('name'), is_vip=js.get('is_vip'))
    return 'Clients create'


@app.route('/clients', methods=['GET'])
def search_clients() -> object:
    """Найти клиента."""
    pr = request.args.get('clientId')
    query = Clients.get_by_id(pr)
    json_data = jsonify(model_to_dict(query))
    return json_data


@app.route('/clients', methods=['DELETE'])
def del_clients() -> str:
    """Удалить клиента."""
    pr = request.args.get('clientId')
    res = Clients.delete_by_id(pr)
    return f'Удален {res} клиент'


@app.route('/orders', methods=['POST'])
def add_orders() -> str:
    """Добавить заказ."""
    js = request.get_json()
    if js.get('status') != 'not_accepted':
        return f'''Заказ не создан. Указан некорректный статус {js.get('status')}'''
    Orders.create(client_id=js.get('client_id'), driver_id=js.get('driver_id'), date_created=js.get('date_created'),
                  status=js.get('status'), address_from=js.get('address_from'), address_to=js.get('address_to'))
    return 'Order create'


@app.route('/orders', methods=['GET'])
def search_orders() -> object:
    """Найти заказ."""
    pr = request.args.get('orderId')
    query = Orders.get_by_id(pr)
    json_data = jsonify(model_to_dict(query))
    return json_data


@app.route('/orders', methods=['PUT'])
def update_order() -> str:
    """Редактировать заказ."""
    js = request.get_json()
    pr = request.args.get('orderId')
    old_el = Orders.get_by_id(pr)
    if js.get('status') not in state:
        return f'''Заказ {pr}. Изменение статуса на {js.get('status')} невозможно'''
    if old_el.status != js.get('status'):
        if old_el.status in ('done', 'cancelled'):
            return f'Заказ {pr} в статусе {old_el.status}. Изменение статуса невозможно'
        if old_el.status == 'in_progress':
            if js.get('status') not in ('done', 'cancelled'):
                return f'''Заказ {pr} в статусе {old_el.status}. Изменение статус на {js.get('status')} невозможно'''
        if old_el.status == 'not_accepted':
            if js.get('status') not in ('in_progress', 'cancelled'):
                return f'''Заказ {pr} в статусе {old_el.status}. Изменение статус на {js.get('status')} невозможно'''
    if old_el.date_created != js.get('date_created')\
            or old_el.client_id != js.get('client_id')\
            or old_el.driver_id != js.get('driver_id'):
        if old_el.status != 'not_accepted':
            return f'''Заказ {pr}. Данные изменить нелья, тк заказ в статусе {old_el.status}'''
    query = Orders.update(client_id=js.get('client_id'), driver_id=js.get('driver_id'),
                          date_created=js.get('date_created'),
                          status=js.get('status'), address_from=js.get('address_from'),
                          address_to=js.get('address_to')) \
        .where(id == pr)
    query.execute()
    return 'Заказ обновлен'


app.run(host='0.0.0.0', port=5000)
