from .fixtures import app, client, db
from monolith.models import Operator

from urllib.parse import urlparse
import datetime


def test_create_operator_view_is_available(client):
    res = client.get("/create_operator")
    assert res.status_code == 200


def test_create_operator_view(client, db):
    res = add_operator(client)

    fetched_user = (
        db.session.query(Operator).filter(Operator.email == "operator@mail.com").first()
    )

    assert res.status_code == 302
    assert fetched_user.email == "operator@mail.com"
    assert fetched_user.firstname == "operator"
    assert fetched_user.lastname == "operator"
    assert fetched_user.dateofbirth == datetime.datetime(2020, 12, 5)
    assert urlparse(res.location).path == "/"


# Helpers methods


def add_operator(client):
    return client.post(
        "/create_operator",
        data=dict(
            email="operator@mail.com",
            firstname="operator",
            lastname="operator",
            dateofbirth="05/12/2020",
            password="1233454",
            fiscal_code="123123123123",
        ),
        follow_redirects=False,
    )