import logging
import os
from http import HTTPStatus

import requests
from pydantic import BaseModel


class SMSMessage(BaseModel):
    id: int
    phone: str
    text: str


class SMSender:
    def __init__(self, logger: logging.Logger = None) -> None:
        self.logger = logger
        self.url = os.environ.get("SMS_SERVICE")
        self.token = os.environ.get("SMS_SERVICE_TOKEN")
        self.method = "sms"

    def send(self, data: SMSMessage) -> bool:
        response = requests.post(
            f"{self.url}/{data.id}",
            headers={"Authorization": f"Bearer {self.token}"},
            json=data.dict()
        )

        if response.status_code == HTTPStatus.OK:
            return True
        return False
