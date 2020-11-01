from datetime import date
from monolith.models.health_authority import HealthAuthority
from monolith.models import User
from monolith.services import mock

# DATA

user = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth=date(1995, 12, 31),
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

user2 = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth="31/12/1995",
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

operator = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="01/01/1963",
    fiscal_code="YLLGPP63A01B519O",
)

health_authority = dict(
    email="canicatti@asl.it",
    name="ASL Canicattì",
    password="cani123",
    phone="0808403849",
    country="Italy",
    state="AG",
    city="Canicattì",
    lat=37.36,
    lon=13.84,
)

health_authority2 = dict(
    email="roma@asl.it",
    name="ASL Roma",
    password="romasqpr",
    phone=" 0639741322",
    country="Italy",
    state="RM",
    city="Roma",
    lat=41.89,
    lon=12.49,
)

restaurant = dict(
    name="Trattoria da Fabio",
    phone=555123456,
    lat=40.720586,
    lon=10.10,
    time_of_stay=30,
    operator_id=1,
)

table = dict(name="A10", seats=10, restaurant_id=1)

# CREATION


def create_user(client, data=user2):
    return client.post(
        "/create_user",
        data=data,
        follow_redirects=False,
    )


# ! It's here just as a reference. The testing procedure should not need to work directly
# !     with the database when a view to insert the user is available.
# TODO in the future if not needed, and the test goes as planned, it can be deleted.
def insert_user(db, data=user) -> User:
    temp = User(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


def insert_restaurant_db():
    mock.restaurant()


def create_operator(client, data=operator):
    return client.post(
        "/create_operator",
        data=data,
        follow_redirects=False,
    )


def create_health_authority(client, data=health_authority):
    return client.post(
        "/create_authority",
        data=data,
        follow_redirects=False,
    )


def create_restaurant(client, data=restaurant):
    return client.post(
        "/create_restaurant",
        data=data,
        follow_redirects=False,
    )


def operator_restaurants(client):
    return client.get(
        "/operator/restaurants",
        follow_redirects=False
    )


def create_table(client, restaurant_id=1, data=table):
    return client.post(
        "/operator/restaurants/" + str(restaurant_id) + "/create_table",
        data=data,
        follow_redirects=False,
    )


def edit_table(client, restaurant_id=1, table_id=1, data=table):
    return client.post(
        "/operator/restaurants/"
        + str(restaurant_id)
        + "/tables/"
        + str(table_id)
        + "/edit_table",
        data=data,
        follow_redirects=False,
    )


def delete_table(client, restaurant_id=1, table_id=1, data=table):
    return client.post(
        "/operator/restaurants/"
        + str(restaurant_id)
        + "/tables/"
        + str(table_id)
        + "/delete_table",
        data=data,
        follow_redirects=False,
    )


def insert_health_authority(db, data=health_authority) -> HealthAuthority:
    temp = HealthAuthority(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


# OTHER


def login_user(client, data=user):
    return client.post(
        "/login",
        data=data,
        follow_redirects=False,
    )


def login_operator(client, data=operator):
    return client.post(
        "/operator_login",
        data=data,
        follow_redirects=False,
    )


def logout_operator(client):
    return client.get(
        "/logout",
        follow_redirects=False,
    )


def login_authority(client, data=health_authority):
    return client.post(
        "/authority_login",
        data=data,
        follow_redirects=False,
    )