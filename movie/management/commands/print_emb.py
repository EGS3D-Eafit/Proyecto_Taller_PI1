from django.core.management import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Print one and only one embedding of a movie"
    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        self.stdout.write(self.style.SUCCESS(f"Embeding de {movies[0].title}: {movies[0].emb}"))