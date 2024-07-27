from django.contrib import admin

# Register your models here.
from .models.Equipment import Equipment
from .models.Material import Material
from .models.Ppe import Ppe
from .models.Tool import Tool
from .models.Worker import Worker

admin.site.register(Equipment)
admin.site.register(Material)
admin.site.register(Ppe)
admin.site.register(Tool)
admin.site.register(Worker)