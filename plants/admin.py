from django.contrib import admin
from .models import Plant, PlantPost
# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    fields = ('plant_id', ('common_name', 'scientific_name'), 'ca_native')
    list_display = ('plant_id')

class PlantPostAdmin(admin.ModelAdmin):
    fields = ('post_id', 'post_date', 'plant_id', 'platform', 'related_tag', 'content')
    list_display = ('post_id')


admin.site.register(Plant)
admin.site.register(PlantPost)
