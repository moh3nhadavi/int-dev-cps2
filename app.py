from flask import Flask, g, jsonify, request, url_for
# import requests

app = Flask(__name__)

from database import *
from models import *


@app.route('/')
def hello_world():
    # print(Services.query.all())
    return "Hello CPS2"


@app.route('/rules/', methods=['GET', 'POST'])
def rules():
    # db = get_db()

    if request.method == 'POST':
        json_data = request.get_json()
        conditions = json_data['conditions']
        action = json_data['action']
        db.execute('INSERT INTO rules(conditions, action) values (?,?)',
                   [conditions, action])
        db.commit()

    cur = db.execute('select * from rules')
    rules = cur.fetchall()

    return_values = []
    for rule in rules:
        return_values.append({
            'id': rule['id'],
            'conditions': rule['conditions'],
            'action': rule['action'],
        })

    return jsonify({'rules': return_values})


@app.route('/rules/<int:rule_id>', methods=['GET', 'PATCH'])
def get_rule(rule_id):
    # db = get_db()

    if request.method == 'PATCH':
        json_data = request.get_json()
        conditions = json_data['conditions']
        action = json_data['action']

        db.execute('update rules set conditions = ?, action = ? where id = ?',
                   [conditions, action, rule_id])
        db.commit()

    cur = db.execute(
        'select * from rules where id = ?', [rule_id])

    rule = cur.fetchone()
    return jsonify({'rule': {
        'id': rule['id'],
        'conditions': rule['conditions'],
        'action': rule['action'],
    }})


@app.route('/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    # db = get_db()
    db.execute('delete from rules where id = ?', [rule_id])
    db.commit()
    return jsonify({'message': 'Rule has been deleted successfully!'})


@app.route('/services/', methods=['GET', 'POST'])
def services():
    global db

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
            'icon_url': url_for('static', filename=service.icon_url)
        })

    return jsonify(return_values)


if __name__ == '__main__':
    app.run(debug=True)
