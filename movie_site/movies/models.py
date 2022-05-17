from django.db import models
from datetime import date

# Create your models here.
class Category(models.Model):
    # Create models Категории
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Aktor(models.Model):
    # Create models Актеры
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Актер и режиссер"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    # Create models Жанры
    name = models.CharField("Название жанра", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movis(models.Model):
    # Create models Фильмы
    title = models.CharField("Название фильма", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    yers = models.PositiveSmallIntegerField("Дата выхода", default=2022)
    country = models.CharField("", max_length=30)
    directors = models.ManyToManyField(Aktor, verbose_name="Режиссер", related_name="film_directors") # Зависемость многие к многим !!
    actors = models.ManyToManyField(Aktor, verbose_name="Актер", related_name="film_actors") # Зависемость многие к многим !!
    ganres = models.ManyToManyField(Genre, verbose_name="Жанр") # Зависемость многие к многим !!
    word_premiere = models.DateField("Примера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Укажите сумму в тысячах долларах")
    fess_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="Укажите сумму в тысячах долларах")
    fess_in_word = models.PositiveIntegerField("Сборы в мире", default=0, help_text="Укажите сумму в тысячах долларах")
    category = models.ForeignKey(Category, verbose_name = "Категория", on_delete=models.SET_NULL, null=True) # Зависемость многие к одному !!
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movies_shots/")
    movie = models.ForeignKey(Movis, verbose_name = "Фильм", on_delete=models.CASCADE) # Зависемость многие к одному !!

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStars(models.Model):
    value = models.SmallIntegerField("Числовое значение", default=0)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, verbose_name = "Звезда рейтинга")
    movie = models.ForeignKey(Movis, on_delete=models.CASCADE, verbose_name = "Фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"
    
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name = "Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movis, on_delete=models.CASCADE, verbose_name = "Фильм")

    def __str__(self):
        return f"{self.name} - {self.movie}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"