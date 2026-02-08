from flask import Blueprint, request
from app.models.user import UserModel
from app.utils.security import generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Аутентификация пользователя

    Тело запроса:
        - id: идентификатор пользователя
        - password: пароль

    Статусы:
        - 200: {"token": "..."}
        - 400: Invalid request data
        - 404: User not found
        - 500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return {'message': 'Invalid request data'}, 400

        user_id = data.get('id')
        password = data.get('password')

        if not user_id or not password:
            return {'message': 'id and password are required'}, 400

        user = UserModel.authenticate(user_id, password)

        if not user:
            return {'message': 'User not found or invalid password'}, 404

        token = generate_token(user_id)
        return {'token': token}, 200

    except Exception as e:
        return {'message': 'Internal server error', 'error': str(e)}, 500
