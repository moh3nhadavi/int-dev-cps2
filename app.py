from flask import Flask, g, request, jsonify
from database import get_db, connect_db
import requests

app = Flask(__name__)


def get_current_status():
    x = requests.get("")
    if x.status_code == 200:
        return x.text
    else:
        return False


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def hello_world():
    return get_current_status()


@app.route('/rules/', methods=['GET', 'POST'])
def rules():
    db = get_db()

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
    db = get_db()

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
    db = get_db()
    db.execute('delete from rules where id = ?', [rule_id])
    db.commit()
    return jsonify({'message': 'Rule has been deleted successfully!'})



@app.route('/services/',methods=['GET','POST'])
def services():
    db = get_db()

    if request.method == 'POST':
        json_data = request.get_json()
        # name = json_data['conditions']
        # action = json_data['action']
        # db.execute('INSERT INTO rules(conditions, action) values (?,?)',
        #            [conditions, action])
        # db.commit()

    cur = db.execute('select * from services')
    services = cur.fetchall()

    return_values = []
    for service in services:
        return_values.append({
            'id': service['id'],
            'name' : service['name'],
            'icon_url' : service['icon_url']
        })

    return jsonify(return_values)

if __name__ == '__main__':
    app.run(debug=True)
