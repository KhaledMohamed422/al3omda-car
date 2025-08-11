from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        pass 
        # from core.models.shared import Category, TruckType, Country
        # from offers.models import Offer
        # from products.models import Product
        # from products.signals.slugify import register_slugify_model

        # register_slugify_model(Category, 'name')
        # register_slugify_model(TruckType, 'name')
        # register_slugify_model(Country, 'country_name_ar')
        # register_slugify_model(Product, 'name')
        # register_slugify_model(Offer, 'name')
