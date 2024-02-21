from pydantic import BaseModel


class WSLinkModel(BaseModel):
    """Модель ссылки на вебсокет."""

    link: str
