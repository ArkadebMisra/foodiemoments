from django.contrib import admin
from .models import Image,Comment

# Register your models here

class ImageAdmin(admin.ModelAdmin):
    list_display = ['user','slug','image','about','created',]
    list_filter = ['created']


admin.site.register(Image,ImageAdmin)
admin.site.register(Comment)
