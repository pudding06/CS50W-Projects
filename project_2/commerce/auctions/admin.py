from django.contrib import admin
from .models import User, Category, Listings, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Comment)