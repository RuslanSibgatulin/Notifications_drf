import uuid
from datetime import datetime

from pydantic import BaseModel, SecretStr


class Task(BaseModel):
    mailing_id: uuid.UUID
    client_id: uuid.UUID
    msg: str
    phone: SecretStr
    stop_client: datetime

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value()
        }
