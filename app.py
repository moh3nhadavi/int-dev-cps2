from flask import Flask, g, jsonify, request, url_for

app = Flask(__name__)

from database import *
from models import *


@app.route('/')
def hello_world():
    return "Hello CPS2"


@app.route('/services/', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        icon_url = json_data['icon_url']
        service = Services(name=name, icon_url=icon_url)
        db.session.add(service)
        db.session.commit()

    services = Services.query.all()
    return_values = []
    for service in services:
        return_values.append({
            'id': service.id,
            'name': service.name,
            'icon_url': service.icon_url
        })

    return jsonify(return_values)


@app.route('/services/<int:service_id>', methods=['GET', 'PATCH'])
def get_service(service_id):
    service = Services.query.get_or_404(service_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        icon_url = json_data['icon_url']

        service.name = name
        service.icon_url = icon_url

        db.session.add(service)
        db.session.commit()

    return jsonify({
        'id': service.id,
        'name': service.name,
        'icon_url': service.icon_url
    })


@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service has been deleted successfully!'})


@app.route('/devices/services/<int:service_id>', methods=['GET', 'POST'])
def devices(service_id):
    service = Services.query.get_or_404(service_id)
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        device = Devices(name=name, service=service)
        db.session.add(device)
        db.session.commit()

    devices = Devices.query.filter_by(service_id=service_id)
    return_values = []
    for device in devices:
        return_values.append({
            'id': device.id,
            'name': device.name,
            'service_id': device.service_id
        })

    return jsonify(return_values)


@app.route('/devices/<int:device_id>', methods=['GET', 'PATCH'])
def get_device(device_id):
    device = Devices.query.get_or_404(device_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        service_id = int(json_data['service_id'])
        service = Services.query.get_or_404(service_id)
        device.name = name
        device.service = service

        db.session.add(device)
        db.session.commit()

    return jsonify({
        'id': device.id,
        'name': device.name,
        'service_id': device.service_id
    })


@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Devices.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device has been deleted successfully!'})


@app.route('/conditions/devices/<int:device_id>', methods=['GET', 'POST'])
def conditions(device_id):
    device = Devices.query.get_or_404(device_id)
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        type = json_data['type']
        condition = Conditions(name=name, type=type, device=device)
        db.session.add(condition)
        db.session.commit()

    conditions = Conditions.query.filter_by(device_id=device_id)
    return_values = []
    for condition in conditions:
        return_values.append({
            'id': condition.id,
            'name': condition.name,
            'type': condition.type,
            'device_id': condition.device_id
        })

    return jsonify(return_values)


@app.route('/conditions/<int:condition_id>', methods=['GET', 'PATCH'])
def get_condition(condition_id):
    condition = Conditions.query.get_or_404(condition_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        type = json_data['type']
        device_id = int(json_data['device_id'])
        device = Devices.query.get_or_404(device_id)
        condition.name = name
        condition.type = type
        condition.device = device

        db.session.add(condition)
        db.session.commit()

    return jsonify({
        'id': condition.id,
        'name': condition.name,
        'type': condition.type,
        'device_id': condition.device_id
    })


@app.route('/conditions/<int:condition_id>', methods=['DELETE'])
def delete_condition(condition_id):
    condition = Conditions.query.get_or_404(condition_id)
    db.session.delete(condition)
    db.session.commit()
    return jsonify({'message': 'Condition has been deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
