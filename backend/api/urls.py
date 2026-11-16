from django.urls import path

from . import views

urlpatterns = [
    path("current/<str:tier>", views.leaderboard, {"table": "current"}),
    path("previous/<str:tier>", views.leaderboard, {"table": "previous"}),
    path("older/<str:tier>", views.leaderboard, {"table": "tma"}),
    path("login", views.login),
    path("register", views.register),
    path("saveteam", views.save_team),
    path("dex/<str:name>", views.dex),
]
