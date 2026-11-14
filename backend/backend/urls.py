from django.urls import include, path

urlpatterns = [
    path("apiv1/", include("api.urls")),
]
