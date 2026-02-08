from dataclasses import dataclass
from typing import Any


@dataclass
class UserResponseModel:
    """Модель ответа пользователя с фиксированным порядком полей."""
    id: str
    first_name: str
    second_name: str
    birthdate: str | None
    gender: str | None
    biography: str | None
    city: str | None

    @classmethod
    def from_db(cls, data: dict) -> 'UserResponseModel':
        """Создание модели из данных БД."""
        birthdate = data.get('birthdate')
        if birthdate and hasattr(birthdate, 'isoformat'):
            birthdate = birthdate.isoformat()

        return cls(
            id=data['id'],
            first_name=data['first_name'],
            second_name=data['second_name'],
            birthdate=birthdate,
            gender=data.get('gender'),
            biography=data.get('biography'),
            city=data.get('city')
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь с сохранением порядка полей."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'birthdate': self.birthdate,
            'gender': self.gender,
            'biography': self.biography,
            'city': self.city
        }
