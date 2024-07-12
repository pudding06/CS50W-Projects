from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listings", views.create_listings, name="create_listings"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add/<int:id>", views.add, name="add"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("display_category", views.display_category, name="display_category"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid")
]