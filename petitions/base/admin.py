from django.contrib import admin
from .models import Topic, Petition, User

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Petition)
