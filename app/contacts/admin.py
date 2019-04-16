from django.contrib import admin
from .models import Person, Phone, Email, Address, Group


admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Group)



