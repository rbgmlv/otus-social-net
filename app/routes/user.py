from flask import Blueprint, request
from app.models.user import UserModel
from datetime import datetime

user_bp = Blueprint('user', __name__)


def validate_date(date_string: str) -> bool:
    """Валидация для строки с днем рождения (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@user_bp.route('/user/register', methods=['POST'])
def register():
    """
    Регистрация нового пользователя.

    Тело запроса:
        - first_name: имя
        - second_name: фамилия
        - birthdate: день рождения (YYYY-MM-DD)
        - gender: пол
        - biography: биография/интересы пользователя
        - city: город
        - password: пароль

    Статусы:
        - 200: {"user_id": "..."}
        - 400: Invalid request data
        - 500: Server error
    """
    try:
        data = request.get_json()

        if not data:
            return {'message': 'Invalid request data'}, 400

        required_fields = ['first_name', 'second_name', 'birthdate', 'gender', 'biography', 'city', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 400

        if not validate_date(data['birthdate']):
            return {'message': 'Invalid birthdate format. Use YYYY-MM-DD'}, 400

        user_id = UserModel.create(
            first_name=data['first_name'],
            second_name=data['second_name'],
            birthdate=data['birthdate'],
            gender=data['gender'],
            biography=data['biography'],
            city=data['city'],
            password=data['password']
        )

        return {'user_id': user_id}, 200

    except Exception as e:
        return {'message': 'Internal server error', 'error': str(e)}, 500


@user_bp.route('/user/get/<user_id>', methods=['GET'])
def get_user(user_id: str):
    """
    Получение анкеты пользователя по user_id.

    Path-параметры:
        - user_id: идентификатор пользователя

    Статусы:
        - 200: объект с пользователем
        - 400: Invalid request
        - 404: User not found
        - 500: Server error
    """
    try:
        if not user_id:
            return {'message': 'User ID is required'}, 400

        user = UserModel.get_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, 404

        return user, 200

    except Exception as e:
        return {'message': 'Internal server error', 'error': str(e)}, 500
