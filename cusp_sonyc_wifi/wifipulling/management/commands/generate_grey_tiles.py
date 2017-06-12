from django.core.management.base import BaseCommand
from wifipulling.lib import generateGreyTiles

class Command(BaseCommand):
    help = 'Generates and saves tiles for all the locations'

    def handle(self, *args, **options):    
        generateGreyTiles()
