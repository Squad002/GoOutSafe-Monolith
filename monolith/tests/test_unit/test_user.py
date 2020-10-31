from ..fixtures import db, app
from .. import helpers

from datetime import datetime, timedelta


def test_has_been_marked_should_be_true(db):
    ha = helpers.insert_health_authority(db)
    user = helpers.insert_user(db)
    ha.mark(user)
    db.session.commit()

    assert user.has_been_marked()


def test_is_marked_should_be_true(db):
    ha = helpers.insert_health_authority(db)
    user = helpers.insert_user(db)
    ha.mark(user)
    db.session.commit()

    assert user.is_marked()


def test_has_been_marked_should_be_false(db):
    helpers.insert_health_authority(db)
    user = helpers.insert_user(db)
    db.session.commit()

    assert not user.has_been_marked()


def test_get_mark_expiration_date_should_be_8_days_from_now(db):
    ha = helpers.insert_health_authority(db)
    user = helpers.insert_user(db)
    ha.mark(user, duration=7)
    db.session.commit()

    unmark_date = user.get_mark_expiration_date()

    assert unmark_date.date() == (datetime.utcnow() + timedelta(days=8)).date()


def test_get_remaining_mark_days(db):
    ha = helpers.insert_health_authority(db)
    user = helpers.insert_user(db)
    ha.mark(user, starting_date=datetime(2020, 10, 1), duration=14)
    db.session.commit()

    remaining_days = user.get_remaining_mark_days(from_date=datetime(2020, 10, 10))

    print(user.get_mark_expiration_date())

    assert remaining_days == 5


def test_get_last_mark_duration_should_be_ten(db):
    user = helpers.insert_user(db)

    ha1 = helpers.insert_health_authority(db)
    ha1.mark(user, starting_date=datetime(2020, 10, 1), duration=14)

    ha2 = helpers.insert_health_authority(db, data=helpers.health_authority2)
    ha2.mark(user, starting_date=datetime(2020, 10, 2), duration=10)

    assert user.get_last_mark_duration() == 10
