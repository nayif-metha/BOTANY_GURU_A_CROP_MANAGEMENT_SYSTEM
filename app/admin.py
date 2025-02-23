from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(registration_db)
admin.site.register(login_db)
admin.site.register(product_db)
admin.site.register(order_db)
admin.site.register(PasswordReset)