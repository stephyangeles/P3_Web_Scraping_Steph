from django.core.management.base import BaseCommand
from scraper.services.scrape import scrape_colors
from scraper.models import Color

class Command(BaseCommand):
    help = "Run the color scraper"

    def handle(self, *args, **kwargs):
        colors = scrape_colors()
        print("Scraped Colors:", colors) 
        
        for color in colors:
            obj, created = Color.objects.get_or_create(
                hex_code=color["hex"],  
                defaults={
                    "name": color["name"],
                    "rgb": color["rgb"],
                    "image": color["image"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {color['name']} ({color['hex']})"))

        self.stdout.write(self.style.SUCCESS("Scraping completed!"))
