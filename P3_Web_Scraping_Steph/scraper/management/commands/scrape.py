from django.core.management.base import BaseCommand
from scraper.services.scrape import scrape_colors, scrape_palettes
from scraper.models import Color, Palette, PaletteColor

class Command(BaseCommand):
    help = "Run the color and palette scraper"

    def handle(self, *args, **kwargs):
        
        colors = scrape_colors()
        print("Scraped Colors:", colors)

        color_objects = {}  
        for color in colors:
            obj, created = Color.objects.get_or_create(
                hex_code=color["hex"],
                defaults={
                    "names": color["name"],
                    "rgb": color["rgb"],
                    "image": color["image"],
                    "source": color.get("source", "")
                }
            )
            color_objects[color["hex"]] = obj  
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Color: {color['name']} ({color['hex']})"))

  

        palettes = scrape_palettes()
        print("Scraped Palettes:", palettes)

        for palette in palettes:
            palette_obj, created = Palette.objects.get_or_create(
                palette_code=palette["code"],
                defaults={
                    "image": palette["image"],
                    "source": palette.get("source", "")
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Palette: {palette['code']}"))

          
          

            colors_in_palette = palette["colors"]
            if len(colors_in_palette) >= 3:
                PaletteColor.objects.create(
                    palette=palette_obj,
                    color1=color_objects[colors_in_palette[0]],
                    color2=color_objects[colors_in_palette[1]],
                    color3=color_objects[colors_in_palette[2]],
                    color4=color_objects[colors_in_palette[3]] if len(colors_in_palette) > 3 else None
                )

        self.stdout.write(self.style.SUCCESS("Scraping completed!"))
