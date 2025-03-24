from django.db import models

class Color(models.Model):
    hex_code = models.CharField(max_length=7, unique=True)  # Ej: #FFFFFF
    rgb = models.CharField(max_length=20)  # Ej: rgb(255, 255, 255)
    names = models.TextField(max_length=100, default="Unknown")  # Ej: White, Blanco, Blanc
    image = models.ImageField(upload_to='src/images/colors/')
    source = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.names.split(',')[0]} ({self.hex_code})"

class Palette(models.Model):
    palette_code = models.CharField(max_length=30, null=True, blank=True)  # Ej: data-code="f1e7e7e69db8ffd0c7fffece"
    image = models.ImageField(upload_to='src/images/palettes/', null=True, blank=True)
    source = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Palette {self.palette_code}"

class PaletteColor(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE)
    color1 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palette_color1')
    color2 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palette_color2')
    color3 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palette_color3')
    color4 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palette_color4', null=True, blank=True)  

    def __str__(self):
        return f"Palette {self.palette.palette_code}: {self.color1.hex_code}, {self.color2.hex_code}, {self.color3.hex_code}, {self.color4.hex_code if self.color4 else ''}"