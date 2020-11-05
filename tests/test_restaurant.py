from .fixtures import app, client, db
from . import helpers
from monolith.models import Restaurant, Table, RestaurantsPrecautions, Precautions
from monolith.models.menu import Menu, Food, MenuItems

from urllib.parse import urlparse


def test_create_restaurant_view_is_available_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 200


def test_create_restaurant_view_is_notavailable_anonymous(client):
    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_create_restaurant_view_is_notavailable_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_create_restaurant_view_is_notavailable_ha(client):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_restaurant_sheet(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.restaurant_sheet(client)
    restaurant = db.session.query(Restaurant).filter_by(id=1).first()

    restaurant_precautions = (
        db.session.query(Precautions.name)
        .filter(
            Precautions.id == RestaurantsPrecautions.precautions_id,
            RestaurantsPrecautions.restaurant_id == 1,
        )
        .all()
    )

    assert res.status_code == 200

    for prec in restaurant_precautions:
        assert bytes(prec.name, "utf-8") in res.data

    assert bytes(restaurant.name, "utf-8") in res.data
    assert bytes(restaurant.cuisine_type.value, "utf-8") in res.data
    assert bytes(str(restaurant.opening_hours), "utf-8") in res.data
    assert bytes(str(restaurant.closing_hours), "utf-8") in res.data
    assert bytes(str(restaurant.phone), "utf-8") in res.data
    for menu in restaurant.menus:
        assert bytes(menu.name, "utf-8") in res.data


def test_create_restaurant(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    res = helpers.create_restaurant(client)

    fetched_restaurant = (
        db.session.query(Restaurant).filter_by(id=1, operator_id=1).first()
    )

    assert res.status_code == 302
    assert fetched_restaurant.name == "Trattoria da Fabio"
    assert fetched_restaurant.phone == 555123456
    assert fetched_restaurant.lat == 40.720586
    assert fetched_restaurant.lon == 10.10
    assert fetched_restaurant.time_of_stay == 30
    assert fetched_restaurant.opening_hours == 12
    assert fetched_restaurant.closing_hours == 24
    assert fetched_restaurant.cuisine_type.name == "ETHNIC"
    assert fetched_restaurant.operator.id == 1
    assert urlparse(res.location).path == "/operator/restaurants"


def test_create_restaurant_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)

    data = dict(
        name="Trattoria da Pippo",
        phone=651981916,
        lat=-500.75,
        lon=900.98,
        time_of_stay=200,
        operator_id=1,
    )

    res = helpers.create_restaurant(client, data)
    fetched_restaurant = db.session.query(
        Restaurant).filter_by(operator_id=1).first()

    assert fetched_restaurant is None
    assert res.status_code == 400


def test_create_duplicate_restaurant(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    restaurant = dict(
        name="Trattoria da Pippo",
        phone=615543,
        lat=40.720586,
        lon=10.10,
        time_of_stay=30,
        cuisine_type="ETHNIC",
        opening_hours=12,
        closing_hours=24,
        operator_id=1,
    )

    res = helpers.create_restaurant(client, restaurant)
    fetched_dup_restaurant = db.session.query(
        Restaurant).filter_by(id=2).first()

    assert res.status_code == 400
    assert fetched_dup_restaurant is None


def test_create_table_view_is_available_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    q = helpers.insert_restaurant_db(db)

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 200


def test_create_table_view_is_notavailable_anonymous(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)
    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_user(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)

    helpers.create_user(client)
    helpers.login_user(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_ha(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)

    helpers.create_health_authority(client)
    helpers.login_authority(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.create_table(client)
    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 302
    assert fetched_table.name == "A10"
    assert fetched_table.seats == 10
    assert urlparse(res.location).path == "/restaurants/1/tables"


def test_create_table_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    data = dict(name="A10", seats=-5, restaurant_id=1)
    res = helpers.create_table(client, data=data)

    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 400
    assert fetched_table is None


def test_create_duplicate_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)
    data = dict(name="A10", seats=2, restaurant_id=1)
    res = helpers.create_table(client, data=data)

    fetched_table = db.session.query(Table).filter_by(id=2).first()

    assert res.status_code == 400
    assert fetched_table is None


def test_create_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="1963-01-01",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.login_operator(client, data)
    res = helpers.create_table(client)
    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 401
    assert fetched_table is None


def test_delete_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)
    res = helpers.delete_table(client)

    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 200
    assert fetched_table is None


def test_delete_table_not_exists(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.delete_table(client)

    assert res.status_code == 400


def test_delete_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="1963-01-01",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.login_operator(client, data)
    res = helpers.delete_table(client)
    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 401
    assert fetched_table is not None


def test_delete_table_bad_table_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.delete_table(client, table_id=9)

    assert res.status_code == 400


def test_delete_table_bad_restaurant_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.delete_table(client, restaurant_id=5, table_id=1)

    assert res.status_code == 401


def test_edit_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)

    data = dict(id=1, name="A5", seats=6)
    res = helpers.edit_table(client, data=data)

    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 302
    assert fetched_table.name == "A5"
    assert fetched_table.seats == 6
    assert urlparse(res.location).path == "/restaurants/1/tables"


def test_edit_table_to_one_with_same_name(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)

    data = dict(name="A5", seats=6)
    helpers.create_table(client, data=data)

    data["name"] = "A10"
    data["seats"] = 1
    res = helpers.edit_table(client, table_id=2, data=data)

    fetched_table = db.session.query(Table).filter_by(id=2).first()

    assert res.status_code == 400
    assert fetched_table.name == "A5"
    assert fetched_table.seats == 6


def test_edit_table_not_exists(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.edit_table(client)

    assert res.status_code == 400


def test_edit_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    op_data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="1963-01-01",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, op_data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.login_operator(client, op_data)

    table_data = dict(id=1, name="A1", seats=1)
    res = helpers.edit_table(client, table_data)
    fetched_table = db.session.query(Table).filter_by(id=1).first()

    assert res.status_code == 401
    assert fetched_table.name != "A1"
    assert fetched_table.seats != 1


def test_edit_table_bad_restaurant_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.edit_table(client, restaurant_id=2)

    assert res.status_code == 401


def test_edit_table_bad_table_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.edit_table(client, table_id=2)

    assert res.status_code == 400


def test_edit_table_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    bad_table = dict(name="A10", seats=-10)

    res = helpers.edit_table(client, data=bad_table)

    assert res.status_code == 400


def test_operator_view_isavailable_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/operator/restaurants")
    assert res.status_code == 200


def test_operator_view_isnotavailable_anonymous(client, db):
    res = client.get("/operator/restaurants")
    assert res.status_code == 401


def test_operator_view_isnotavailable_user(client, db):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/operator/restaurants")
    assert res.status_code == 401


def test_operator_view_isnotavailable_ha(client, db):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/operator/restaurants")
    assert res.status_code == 401


def test_operator_restaurant(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.operator_restaurants(client)
    op_restaurants = db.session.query(Restaurant).filter_by(operator_id=1)

    assert res.status_code == 200
    for rest in op_restaurants:
        assert bytes(rest.name, "utf-8") in res.data


def test_operator_restaurant_empty(client, db):
    helpers.create_operator(client)

    op_data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="1963-01-01",
        fiscal_code="UIBCAIUBBVX",
    )
    helpers.create_operator(client, op_data)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.login_operator(client, op_data)
    res = helpers.operator_restaurants(client)
    op_restaurants = db.session.query(Restaurant).filter_by(operator_id=1)

    assert res.status_code == 200
    for rest in op_restaurants:
        assert bytes(rest.name, "utf-8") not in res.data


def test_restaurants_available_anonymous(client):
    res = client.get("/restaurants")
    assert res.status_code == 200


def test_restaurants_available_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/restaurants")
    assert res.status_code == 200


def test_restaurants_available_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/restaurants")
    assert res.status_code == 200


def test_restaurants_available_ha(client):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/restaurants")
    assert res.status_code == 200


def test_restaurants_logged(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants")
    q_rest = db.session.query(Restaurant)

    assert res.status_code == 200
    for rest in q_rest:
        assert bytes(rest.name, "utf-8") in res.data


def test_restaurants_notlogged(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    res = client.get("/restaurants")
    q_rest = db.session.query(Restaurant)

    assert res.status_code == 200
    for rest in q_rest:
        assert bytes(rest.name, "utf-8") in res.data


def test_tables_notavailable_user(client):
    helpers.create_operator(client)
    helpers.create_user(client)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.login_user(client)

    res = client.get("/restaurants/1/tables")
    assert res.status_code == 401


def test_tables_notavailable_anonymous(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    res = client.get("/restaurants/1/tables")
    assert res.status_code == 401


def test_tables_available_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants/1/tables")
    assert res.status_code == 200


def test_tables_notavailable_ha(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/restaurants/1/tables")
    assert res.status_code == 401


def test_tables(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = client.get("/restaurants/1/tables")
    q_table = db.session.query(Table).filter_by(restaurant_id=1)

    assert res.status_code == 200
    for table in q_table:
        assert bytes(table.name, "utf-8") in res.data


def test_tables_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="1963-01-01",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    res = client.get("/restaurants/1/tables")

    assert res.status_code == 401


def test_create_menu_isnotavailable_anonymous(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    res = client.get("/operator/restaurants/1/create_menu")

    assert res.status_code == 401


def test_create_menu_isnotavailable_user(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/operator/restaurants/1/create_menu")

    assert res.status_code == 401


def test_create_menu_isavailable_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/operator/restaurants/1/create_menu")

    assert res.status_code == 200


def test_create_menu_isnotavailable_ha(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout(client)

    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/operator/restaurants/1/create_menu")

    assert res.status_code == 401


def test_create_menu(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.create_menu(client)

    menu = db.session.query(Menu).filter_by(id=1).first()
    food = menu.foods.pop()

    assert res.status_code == 302
    assert menu is not None
    assert menu.restaurant_id == 1
    assert menu.name == helpers.menu["menu_name"]
    assert food.name == helpers.menu["name"]
    assert food.price == helpers.menu["price"]
    assert food.category.name == helpers.menu["category"]
    assert urlparse(res.location).path == "/restaurants/1"


def test_create_duplicate_menu(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_menu(client)
    res = helpers.create_menu(client)

    assert res.status_code == 400


def test_create_menu_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    bad_menu = helpers.menu
    bad_menu["menu_name"] = ""
    res = helpers.create_menu(client, data=bad_menu)
    assert res.status_code == 400

    bad_menu["menu_name"] = "Trial menu1"
    bad_menu["name"] = ""
    res = helpers.create_menu(client, data=bad_menu)
    assert res.status_code == 400

    bad_menu["menu_name"] = "Trial menu2"
    bad_menu["name"] = "Trial food"
    bad_menu["price"] = ""
    res = helpers.create_menu(client, data=bad_menu)
    assert res.status_code == 400

    bad_menu["menu_name"] = "Trial menu3"
    bad_menu["price"] = "-5"
    res = helpers.create_menu(client, data=bad_menu)
    assert res.status_code == 400

    bad_menu["menu_name"] = "Trial menu4"
    bad_menu["price"] = "5"
    bad_menu["category"] = "WRONG_CAT"
    res = helpers.create_menu(client, data=bad_menu)
    assert res.status_code == 400
    bad_menu["category"] = "DRINKS"


def test_show_menu(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_menu(client)

    res = helpers.show_menu(client)
    menu = db.session.query(Menu).filter(
        Menu.restaurant_id == 1, Menu.id == 1).first()

    assert res.status_code == 200
    assert bytes(menu.name, "utf-8") in res.data
    for food in menu.foods:
        assert bytes(food.name, "utf-8") in res.data
        assert bytes(str(food.price), "utf-8") in res.data
        assert bytes(food.category.value, "utf-8") in res.data


def test_restaurants(client, db):
    helpers.insert_restaurant_db(db)
    allrestaurants = db.session.query(Restaurant).all()
    assert len(allrestaurants) == 1


def test_restaurant_booking_is_avaible_logged_user(client,):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/restaurants/1/book_table")
    assert res.status_code == 200


def test_restaurant_booking_not_avaible_ha(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/restaurants/1/book_table")
    assert res.status_code == 401


def test_restaurant_booking_not_avaible_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = client.get("/restaurants/1/book_table")
    assert res.status_code == 401


def test_restaurant_booking_not_avaible_anonymous(client):
    res = client.get("/restaurants/1/book_table")
    assert res.status_code == 401


def test_restaurant_booking(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.create_user(client)
    helpers.login_user(client)

    res = helpers.booking(client)

    assert res.status_code == 302


def test_restaurant_all_tables_booked(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout(client)

    helpers.create_user(client)
    helpers.login_user(client)

    res = helpers.booking(client)
    res = helpers.booking(client)

    assert res.status_code == 500
