from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Churches


# Register your models here.

class ChurchesAdmin(admin.ModelAdmin):
    list_display  = ('username', 'email', 'location', 'umushumba')
    search_fields = ('username', 'email', 'location', 'umushumba')




admin.site.register(Churches, UserAdmin)
#admin.site.register(Churches, ChurchesAdmin)