from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("delete_watchlist/<int:id>", views.delete_watchlist, name="delete_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
