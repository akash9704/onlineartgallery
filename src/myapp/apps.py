from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'

class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
