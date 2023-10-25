from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path('listing/<int:item_id>', views.listing_page, name='listing'),
    path('toggle_watchlist/<int:listing_id>', views.toggle_watchlist, name='toggle_watchlist')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)