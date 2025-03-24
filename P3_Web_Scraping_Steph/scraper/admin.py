from django.contrib import admin
from .models import Color, Palette, PaletteColor


admin.site.register(Color)
admin.site.register(Palette)
admin.site.register(PaletteColor)
