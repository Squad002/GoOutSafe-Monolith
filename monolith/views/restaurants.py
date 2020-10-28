from flask import Blueprint, redirect, render_template, request
from monolith.app import db
from monolith.models import Restaurant, Like, Precautions, RestaurantsPrecautions
from flask_login import current_user, login_user, logout_user, login_required
from ..services.auth import admin_required, current_user
from ..services.forms import UserForm

restaurants = Blueprint("restaurants", __name__)


@restaurants.route("/restaurants")
def _restaurants(message=""):
    allrestaurants = db.session.query(Restaurant)
    return render_template(
        "restaurants.html",
        message=message,
        restaurants=allrestaurants,
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )


@restaurants.route("/restaurants/<restaurant_id>")
def restaurant_sheet(restaurant_id):
    records = (
        db.session.query(Restaurant, Precautions, RestaurantsPrecautions)
        .filter(
            Restaurant.id == int(restaurant_id),
            Restaurant.id == RestaurantsPrecautions.restaurant_id,
            RestaurantsPrecautions.precautions_id == Precautions.id,
        )
        .all()
    )  # Join between tabels Restaurant, RestaurantsPrecautions and Precautions
    restaurant = records[0].Restaurant
    precautions = []
    for record in records:
        precautions.append(record.Precautions.name)
    return render_template(
        "restaurantsheet.html",
        name=restaurant.name,
        likes=restaurant.likes,
        lat=restaurant.lat,
        lon=restaurant.lon,
        phone=restaurant.phone,
        precautions=precautions,
    )


@restaurants.route("/restaurants/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    q = Like.query.filter_by(liker_id=current_user.id, restaurant_id=restaurant_id)
    if q.first() != None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.restaurant_id = restaurant_id
        db.session.add(new_like)
        db.session.commit()
        message = ""
    else:
        message = "You've already liked this place!"
    return _restaurants(message)
