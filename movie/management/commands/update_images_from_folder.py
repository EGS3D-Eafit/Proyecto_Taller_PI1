import os
from django.core.management.base import BaseCommand
from movie.models import Movie  # Asegúrate de que el nombre de tu app sea correcto

class Command(BaseCommand):
    help = "Getting images from a folder and assigning them to movies"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                image_filename = f"m_{movie.title}.png"
                image_path_full = os.path.join(images_folder, image_filename)

                if os.path.exists(image_path_full):
                    # ✅ Guardar solo la ruta relativa desde 'media/'
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Imagen asignada a: {movie.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No se encontró imagen para: {movie.title}"))

            except Exception as e:
                self.stderr.write(f"Error con {movie.title}: {e}")

        self.stdout.write(self.style.SUCCESS("Proceso finalizado"))
