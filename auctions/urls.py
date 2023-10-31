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
    path('listing/<int:listing_id>', views.listing_page, name='listing'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('my_postings', views.my_postings, name='my_postings'),
    path('categories', views.categories, name="categories"),
    path('place_bid', views.place_bid, name='place_bid'),
    path('toggle_watchlist', views.toggle_watchlist, name='toggle_watchlist'),
    path('close_auction', views.close_auction, name="close_auction"),
    path('cancel_auction', views.cancel_auction, name="cancel_auction"),
    path('comment', views.post_comment, name='comment'),
    path('delete_comment/<uuid:comment_id>', views.delete_comment, name='delete_comment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)