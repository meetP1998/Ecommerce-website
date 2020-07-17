from django.contrib import admin
from .models import product,Contact,Orders,OrderUpdate
# Register your models here.
from .models import product
admin.site.register(product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
# admin.site.register(Signup)