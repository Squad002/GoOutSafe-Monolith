from .fixtures import app, client, db
from monolith.models import HealthAuthority

from urllib.parse import urlparse
import datetime


def test_create_operator_view_is_available(client):
    res = client.get("/register/authority")
    assert res.status_code == 200


def test_create_authority_view(client, db):
    res = add_authority(client)

    fetched_user = (
        db.session.query(HealthAuthority)
        .filter(HealthAuthority.email == "aslpisa@mail.com")
        .first()
    )

    assert res.status_code == 302
    assert fetched_user.email == "aslpisa@mail.com"
    assert fetched_user.name == "asl Pisa"
    assert fetched_user.phone == "132123"
    assert fetched_user.country == "Italy"
    assert fetched_user.state == "Toscana"
    assert fetched_user.city == "Pisa"
    assert fetched_user.lat == 23423423.4
    assert fetched_user.lon == 234234234
    assert urlparse(res.location).path == "/"


def test_correct_login(client):
    add_authority(client)

    res = client.post(
        "/login/authority",
        data=dict(
            email="aslpisa@mail.com",
            password="1233454",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 302


# Helpers methods


def add_authority(client):
    return client.post(
        "/register/authority",
        data=dict(
            name="asl Pisa",
            email="aslpisa@mail.com",
            password="1233454",
            phone=132123,
            country="Italy",
            state="Toscana",
            city="Pisa",
            lat=23423423.4,
            lon=234234234,
        ),
        follow_redirects=False,
    )
