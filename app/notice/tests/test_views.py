import random
from datetime import timedelta
from re import findall

from django.test import TestCase
from faker import Faker
from notice.models import Client, Mailing, Tag
from pytz import utc


class ClientsAPIViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        faker = Faker('ru_RU')
        tags = {}
        for tag_name in ['admin', 'manager', 'simple_client', 'vip_client']:
            tag = Tag.objects.create(name=tag_name)
            tags[tag.pk] = tag

        providers_code = [_ for _ in range(900, 930)]
        # Create clients
        for i in range(30):
            code = random.choice(providers_code)
            phone_number = "".join(findall("\\d+", faker.phone_number()))[-7:]
            client = Client.objects.create(
                phone=f"+7{code}{phone_number}",
                provider_code=code,
                tz=f'UTC+0{random.randint(0, 5)}:00'
            )
            client.tag.add(random.choice(list(tags.keys())))

        # Create Mailing list
        for i in range(5):
            start_at = faker.date_time_this_decade(before_now=False)
            start_at = start_at.replace(minute=0, second=0, tzinfo=utc)
            mailing = Mailing.objects.create(
                start_at=start_at,
                msg=f"#{i} Hello, world!",
                stop_at=start_at + timedelta(hours=3)
            )
            mailing.tag.add(random.choice(list(tags.keys())))

    def test_view_clients_list(self):
        resp = self.client.get('/api/v1/clients/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 30)

    def test_view_mailiings_list(self):
        resp = self.client.get('/api/v1/mailings/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 5)
        self.assertEqual(
            list(resp.json()["results"][0].keys()),
            ['id', 'start_at', 'msg', 'tag', 'stop_at']
        )
