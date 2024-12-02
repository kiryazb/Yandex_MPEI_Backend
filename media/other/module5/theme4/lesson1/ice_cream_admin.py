from django.contrib import admin

from .models import Category, Topping, Wrapper, IceCream


admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Wrapper)
admin.site.register(IceCream)
