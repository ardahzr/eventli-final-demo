from django.contrib import admin
from .models import Category,Etkinlik
from mptt.admin import MPTTModelAdmin

# Register your models here.

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",),}

@admin.register(Etkinlik)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title","slug")
    list_display_links = ("title","slug")
    prepopulated_fields = {"slug": ("title",),}
    list_filter = ("title","isActive","category")
    search_fields = ("title","description")

