from flask import Flask, g, jsonify, request, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        ip = json_data['ip']
        device = Devices(name=name, service=service, ip=ip)
        db.session.add(device)
        db.session.commit()

    devices = Devices.query.filter_by(service_id=service_id)
    return_values = []
    for device in devices:
        return_values.append({
            'device_id': device.id,
            'name': device.name,
            'service_id': device.service_id,
            'ip': device.ip
        })

    return jsonify(return_values)


@app.route('/devices/<int:device_id>', methods=['GET', 'PATCH'])
def get_device(device_id):
    device = Devices.query.get_or_404(device_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        ip = json_data['ip']
        service_id = int(json_data['service_id'])
        service = Services.query.get_or_404(service_id)
        device.name = name
        device.ip = ip
        device.service = service

        db.session.add(device)
        db.session.commit()

    return jsonify({
        'device_id': device.id,
        'name': device.name,
        'service_id': device.service_id,
        'ip': device.ip
    })


@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Devices.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device has been deleted successfully!'})


@app.route('/conditions/services/<int:service_id>', methods=['GET', 'POST'])
def conditions(service_id):
    service = Services.query.get_or_404(service_id)
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        type = json_data['type']
        endpoint = None
        request_type = None
        if "endpoint" in json_data:
            endpoint = json_data['endpoint']
        if "request_type" in json_data:
            request_type = json_data['request_type']

        condition = Conditions(name=name, type=type, endpoint=endpoint, request_type=request_type, service=service)
        db.session.add(condition)
        db.session.commit()

    conditions = Conditions.query.filter_by(service_id=service_id)
    return_values = []
    for condition in conditions:
        return_values.append({
            'condition_id': condition.id,
            'name': condition.name,
            'type': condition.type,
            'endpoint': condition.endpoint,
            'request_type': condition.request_type,
            'service_id': condition.service_id
        })

    return jsonify(return_values)


@app.route('/conditions/<int:condition_id>', methods=['GET', 'PATCH'])
def get_condition(condition_id):
    condition = Conditions.query.get_or_404(condition_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        type = json_data['type']
        endpoint = None
        request_type = None
        if "endpoint" in json_data:
            endpoint = json_data['endpoint']
        if "request_type" in json_data:
            request_type = json_data['request_type']
        service_id = int(json_data['service_id'])
        service = Services.query.get_or_404(service_id)
        condition.name = name
        condition.type = type
        condition.endpoint = endpoint
        condition.request_type = request_type
        condition.service = service

        db.session.add(condition)
        db.session.commit()

    return jsonify({
        'condition_id': condition.id,
        'name': condition.name,
        'type': condition.type,
        'endpoint': condition.endpoint,
        'request_type': condition.request_type,
        'service_id': condition.service_id
    })


@app.route('/conditions/<int:condition_id>', methods=['DELETE'])
def delete_condition(condition_id):
    condition = Conditions.query.get_or_404(condition_id)
    db.session.delete(condition)
    db.session.commit()
    return jsonify({'message': 'Condition has been deleted successfully!'})


@app.route('/actions/services/<int:service_id>', methods=['GET', 'POST'])
def actions(service_id):
    service = Services.query.get_or_404(service_id)
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        endpoint = None
        request_type = None
        if "endpoint" in json_data:
            endpoint = json_data['endpoint']
        if "request_type" in json_data:
            request_type = json_data['request_type']
        action = Actions(name=name, endpoint=endpoint, request_type=request_type, service=service)
        db.session.add(action)
        db.session.commit()

    actions = Actions.query.filter_by(service_id=service_id)
    return_values = []
    for action in actions:
        return_values.append({
            'action_id': action.id,
            'name': action.name,
            'endpoint': action.endpoint,
            'request_type': action.request_type,
            'service_id': action.service_id
        })
    return jsonify(return_values)


@app.route('/actions/<int:action_id>', methods=['GET', 'PATCH'])
def get_action(action_id):
    action = Actions.query.get_or_404(action_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        name = json_data['name']
        endpoint = None
        request_type = None
        if "endpoint" in json_data:
            endpoint = json_data['endpoint']
        if "request_type" in json_data:
            request_type = json_data['request_type']
        service_id = int(json_data['service_id'])
        service = Services.query.get_or_404(service_id)
        action.name = name
        action.endpoint = endpoint
        action.request_type = request_type
        action.service = service

        db.session.add(action)
        db.session.commit()

    return jsonify({
        'action_id': action.id,
        'name': action.name,
        'endpoint': action.endpoint,
        'request_type': action.request_type,
        'service_id': action.service_id
    })


@app.route('/actions/<int:action_id>', methods=['DELETE'])
def delete_action(action_id):
    action = Actions.query.get_or_404(action_id)
    db.session.delete(action)
    db.session.commit()
    return jsonify({'message': 'Action has been deleted successfully!'})


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == 'POST':
        json_data = request.get_json()
        condition_id = json_data['condition_id']
        action_id = json_data['action_id']
        condition_value = json_data['condition_value']
        device_id = json_data['device_id']
        condition_type_value = None
        if "condition_type_value" in json_data:
            condition_type_value = json_data['condition_type_value']

        condition = Conditions.query.get_or_404(condition_id)
        action = Actions.query.get_or_404(action_id)
        device = Devices.query.get_or_404(device_id)

        rule = Rules(condition=condition, action=action, device=device, condition_value=condition_value,
                     condition_type_value=condition_type_value)

        db.session.add(rule)
        db.session.commit()

    rules = Rules.query.all()
    return_values = []
    for rule in rules:
        return_values.append({
            'rule_id': rule.id,
            'action': {
                'id': rule.action.id,
                'name': rule.action.name,
                # 'endpoint' : rule.action.endpoint
            },
            'condition': {
                'id': rule.condition.id,
                'name': rule.condition.name,
                'type': rule.condition.type,
            },
            'condition_value': rule.condition_value,
            'condition_type_value': rule.condition_type_value,
        })
    return jsonify(return_values)


@app.route('/rules/<int:rule_id>', methods=['GET', 'PATCH'])
def get_rule(rule_id):
    rule = Rules.query.get_or_404(rule_id)
    if request.method == 'PATCH':
        json_data = request.get_json()
        condition_id = json_data['condition_id']
        action_id = json_data['action_id']
        device_id = json_data['device_id']
        condition_value = json_data['condition_value']
        condition_type_value = None
        if "condition_type_value" in json_data:
            condition_type_value = json_data['condition_type_value']

        condition = Conditions.query.get_or_404(condition_id)
        action = Actions.query.get_or_404(action_id)
        device = Devices.query.get_or_404(device_id)

        rule.action_id = action_id
        rule.condition_id = condition_id
        rule.device_id = device_id
        rule.condition_value = condition_value
        rule.condition_type_value = condition_type_value

        db.session.add(rule)
        db.session.commit()

    return jsonify({
        'rule_id': rule.id,
        'action': {
            'id': rule.action.id,
            'name': rule.action.name,
            # 'endpoint' : rule.action.endpoint
        },
        'condition': {
            'id': rule.condition.id,
            'name': rule.condition.name,
            'type': rule.condition.type,
        },
        'condition_value': rule.condition_value,
        'condition_type_value': rule.condition_type_value,
    })


@app.route('/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    rule = Rules.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'message': 'Rule has been deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
