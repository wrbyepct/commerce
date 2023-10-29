from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .utils import create_default_category

class AuctionsConfig(AppConfig):
    name = 'auctions'
    def ready(self):
        post_migrate.connect(create_default_category, sender=self)

