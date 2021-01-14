from flask import Blueprint, jsonify
from database.models.user import User
from database.db import session
from utils.jsonEncoder import JSONEncoder

users = Blueprint('users', __name__)


@users.route('/users', methods=['GET'])
def getUsers():
    try:
        all_users = session.query(User).all()
        return jsonify(users=JSONEncoder(all_users)), 200
    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500


@users.route('/users/<user_id>', methods=['GET'])
def getUserById(user_id):
    try:
        if not user_id.isdigit(): raise ValueError('Id must be integer')
        user_id = int(user_id)
        if user_id < 1: raise ValueError('Id must be bigger than 0')

        user = session.query(User).get(user_id)
        if user is None: return jsonify({"message": 'Not found'}), 404
        return jsonify(user=JSONEncoder(user)), 200

    except ValueError as err:
        return jsonify({"message": str(err)}), 400

    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500