from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.http import HttpResponse

from .models import Movie

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html', {'name': 'waos'})

def signup(request):
    email = request.POST.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') # Obtener todos los años de las películas
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre') #Obtener todos los generos de las películas
    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_genre = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0].strip()  # Extrae el primer género y elimina espacios
            movies_by_genre = Movie.objects.filter(genre__startswith=first_genre)
        else:
            movies_by_genre = Movie.objects.filter(genre__isnull=True)
            first_genre = "Check Pending"

        count = movies_by_genre.count()
        movie_counts_by_genre[first_genre] = count

    def generate_bar_chart(data_dict, title, xlabel, ylabel):
        bar_width = 0.5
        bar_positions = range(len(data_dict))
        plt.bar(bar_positions, data_dict.values(), width=bar_width, align='center')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(bar_positions, data_dict.keys(), rotation=90)
        plt.subplots_adjust(bottom=0.3)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    graphic1 = generate_bar_chart(movie_counts_by_year, 'Movies per year', 'Year', 'Number of movies')
    graphic2 = generate_bar_chart(movie_counts_by_genre, 'Movies by genre', 'Genre', 'Number of movies')

    return render(request, 'statistics.html', {'graphic_year': graphic1, 'graphic_genre': graphic2})