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


if __name__ == '__main__':
    app.run(debug=True)
