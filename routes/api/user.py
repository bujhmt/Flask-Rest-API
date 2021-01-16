from flask import Blueprint, jsonify, request
from database.models.user import User
from database.db import session
from utils.jsonEncoder import JSONEncoder, getModelKeys

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
        data = request.form
        for key in getModelKeys(User):
            if not key in data: raise AssertionError(f'Property {key} is missing')

        user = User(email=data['email'])
        user.setPassword(data['password'])
        session.add(user)

        session.commit()
        session.refresh(user)

        return jsonify(user=JSONEncoder(user)), 201

    except AssertionError as err:
        return jsonify({"message": str(err)}), 400

    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500

@users.route('/users/<user_id>', methods=['PUT'])
def updateUserById(user_id):
    try:
        if not user_id.isdigit(): raise ValueError('Id must be integer')
        user_id = int(user_id)
        if user_id < 1: raise ValueError('Id must be bigger than 0')

        user = session.query(User).get(user_id)
        if user is None: return jsonify({"message": 'Not found'}), 404

        data = request.form
        for key in getModelKeys(User):
            if key is 'password' and key in data: user.setPassword(data[key])
            else:
                if key in data: user.__setattr__(key, data[key])

        session.commit()
        session.refresh(user)

        return jsonify(user=JSONEncoder(user)), 200

    except ValueError as err:
        return jsonify({"message": str(err)}), 400

    except AssertionError as err:
        return jsonify({"message": str(err)}), 400

    except Exception as err:
        print(err)
        return jsonify({"message": str(err)}), 500