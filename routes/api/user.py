from flask import Blueprint, jsonify, request
from database.models.user import User
from database.db import session
from utils.jsonEncoder import JSONEncoder
from werkzeug.exceptions import BadRequestKeyError

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


@users.route('/users/<user_id>', methods=['DELETE'])
def deleteUserById(user_id):
    try:
        if not user_id.isdigit(): raise ValueError('Id must be integer')
        user_id = int(user_id)
        if user_id < 1: raise ValueError('Id must be bigger than 0')

        user = session.query(User).get(user_id)
        if user is None: return jsonify({"message": 'Not found'}), 404

        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return jsonify(user=JSONEncoder(user)), 200

    except ValueError as err:
        return jsonify({"message": str(err)}), 400

    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500


@users.route('/users', methods=['POST'])
def createUser():
    try:
        if not request.form['email'] or not request.form['password']: raise Exception('Invalid data')

        user = User(email=request.form['email'])
        user.setPassword(request.form['password'])
        session.add(user)

        session.commit()
        session.refresh(user)

        return jsonify(user=JSONEncoder(user)), 201

    except BadRequestKeyError:
        return jsonify({"message": 'Some keys are missing'}), 400

    except AssertionError as err:
        return jsonify({"message": str(err)}), 400

    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500