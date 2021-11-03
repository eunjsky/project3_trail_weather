from django.contrib import admin

# Register your models here.
from .models import Trail, Activity

# Register your models here
admin.site.register(Trail)
admin.site.register(Activity)