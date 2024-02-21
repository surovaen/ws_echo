from pydantic import BaseModel, field_validator


class UserModel(BaseModel):
    """Модель пользователя."""

    username: str
    password: str

    @field_validator('password')
    def check_password(cls, value):
        """Валидация поля 'Пароль'."""
        if len(value) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        if not any(c.isupper() for c in value):
            raise ValueError('Пароль должен содержать хотя бы 1 заглавную букву')
        if not any(c.islower() for c in value):
            raise ValueError('Пароль должен содержать хотя бы 1 строчную букву')
        if not any(c.isdigit() for c in value):
            raise ValueError('Пароль должен содержать хотя бы 1 цифру')
        return value


class TokenModel(BaseModel):
    """Модель токена."""

    token: str
