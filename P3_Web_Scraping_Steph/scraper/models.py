from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=100)  # Nombre del color (ej: "Rojo Carmesí")
    hex_code = models.CharField(max_length=7, unique=True)  # Código HEX (ej: "#FF5733")
    rgb = models.CharField(max_length=20)  # Formato RGB (ej: "rgb(255, 87, 51)")
    image = models.ImageField(upload_to="colors/", blank=True, null=True)  # Imagen de referencia

    def __str__(self):
        return f"{self.name} ({self.hex_code})"

class Palette(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)  # Nombre de la paleta (opcional)
    colors = models.ManyToManyField(Color, related_name="palettes")  # Relación N:M con colores
    source_url = models.URLField()  # Fuente de donde se scrapeó

    def __str__(self):
        return self.name if self.name else f"Paleta {self.id}"
