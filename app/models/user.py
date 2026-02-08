from app.db.connection import execute_query
from app.utils.security import hash_password, verify_password, generate_user_id
from app.utils.response import UserResponseModel


class UserModel:
    """Модель пользователя с прямыми запросами SQL."""

    @staticmethod
    def create(first_name: str, second_name: str, birthdate: str, gender: str,
               biography: str, city: str, password: str) -> str:
        """
        Создание пользователя.

        Возвращает user_id при успешном создании.
        """
        user_id = generate_user_id()
        password_hash = hash_password(password)

        query = """
            INSERT INTO users (id, first_name, second_name, birthdate, gender, biography, city, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (user_id, first_name, second_name, birthdate, gender, biography, city, password_hash)

        execute_query(query, params)
        return user_id

    @staticmethod
    def get_by_id(user_id: str) -> dict | None:
        """
        Получение пользователя по user_id без хэша пароля.
        """
        query = """
            SELECT id, first_name, second_name, birthdate, gender, biography, city
            FROM users
            WHERE id = %s
        """
        result = execute_query(query, (user_id,), fetch_one=True)

        if result:
            return UserResponseModel.from_db(result).to_dict()

        return None

    @staticmethod
    def get_by_id_with_password(user_id: str) -> dict | None:
        """
        Получение пользователя по user_id с хэшем пароля (для аутентификации).
        """
        query = """
            SELECT id, first_name, second_name, birthdate, gender, biography, city, password_hash
            FROM users
            WHERE id = %s
        """
        return execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def authenticate(user_id: str, password: str) -> dict | None:
        """
        Аутентификация пользователя по user_id и паролю.
        """
        user = UserModel.get_by_id_with_password(user_id)

        if user and verify_password(password, user['password_hash']):
            return UserResponseModel.from_db(user).to_dict()

        return None
