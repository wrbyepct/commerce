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
    path('bids', views.bids_on_item, name='bids'),
    path('mybids', views.my_bids, name='mybids'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name="remove_from_watchlist"),
    path('my_postings', views.my_postings, name='my_postings'),
    path('categories', views.categories, name="categories"),
    path('place_bid', views.place_bid, name='place_bid'),
    path('toggle_watchlist/<int:listing_id>', views.toggle_watchlist, name='toggle_watchlist'),
    path('close_auction', views.close_auction, name="close_auction"),
    path('cancel_auction>', views.cancel_auction, name="cancel_auction"),
    path('post_comment', views.post_comment, name='post_comment'),
    path('save_changed_comment/<uuid:comment_id>', views.save_changed_comment, name='save_changed_comment'),
    path('delete_comment/<uuid:comment_id>', views.delete_comment, name='delete_comment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)