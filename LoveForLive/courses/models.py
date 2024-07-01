from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from LoveForLive.settings import MEDIA_ROOT
from PIL import Image


class Courses(models.Model):
    slug = models.SlugField("Название курса", max_length=50, unique=True)
    title = models.CharField('Заголовок курса', max_length=50, default=None)
    description = models.TextField('Описание курса', max_length=500, default='Описание')
    img = models.ImageField("Изображение курса", upload_to='courses', default='default.png')
    price = models.IntegerField('Цена курса', default=0)
    hide = models.BooleanField('Режим отладки', default=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        try:
            this = Courses.objects.get(id=self.id)
            if this.img != self.img and this.img.path != MEDIA_ROOT+'\default.png':
                this.img.delete(save=False)
        except:
            pass
        super().save()
        image = Image.open(self.img.path)
        if image.height > 512 or image.width > 512:
            resize = (512, 512)
            image.thumbnail(resize)
            image.save(self.img.path)
        users = User.objects.all()
        for user in users:
            try:
                Allowance.objects.get(user=user, course=self)
            except Exception:
                Allowance(user=user, course=self, allow=False).save()

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Courses, self).delete(*args, **kwargs)
        if path != MEDIA_ROOT + '\default.png':
            storage.delete(path)
        Allowance.objects.filter(course=self)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Dossing(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    dossing_list = models.TextField('Список дозировок', max_length=10000)

    class Meta:
        verbose_name = 'Дозировки'
        verbose_name_plural = 'Дозировки'


class Allowance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    allow = models.BooleanField("Оплата")

    def __str__(self):
        return f'{self.user.username}_{self.course}'

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступ к курсам'


class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lesson_slug = models.SlugField('Название урока', max_length=80)
    title = models.CharField('Заголовок урока', max_length=50, default=None)
    text = models.TextField('Текстовый материал')
    number = models.IntegerField('Номер урока')
    poster = models.ImageField("Постер для видео", upload_to='posters', default='poster.png')
    video = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        default=None
    )

    def save(self, *args, **kwargs):
        try:
            this = Lesson.objects.get(id=self.id)
            if this.poster != self.poster and this.poster.path != MEDIA_ROOT+'\poster.png':
                this.poster.delete(save=False)
        except:
            pass
        super().save()
        image = Image.open(self.poster.path)
        if image.height > 1000 or image.width > 600:
            resize = (1000, 600)
            image.thumbnail(resize)
            image.save(self.poster.path)

    def delete(self, *args, **kwargs):
        storage, path = self.poster.storage, self.poster.path
        super(Lesson, self).delete(*args, **kwargs)
        if path != MEDIA_ROOT + '\poster.png':
            storage.delete(path)

    def __str__(self):
        return f'{self.course.__str__()}_{self.lesson_slug}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Tasks(models.Model):
    task_text = models.TextField('Текст задания')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.lesson.__str__()

    def save(self, *args, **kwargs):
        super().save()
        users = User.objects.all()
        for user in users:
            LessonProgress(user=user, task=self).save()

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, default=None)
    status = models.BooleanField("Статус задания", default=False)
    feedback = models.TextField('Обратная связь', blank=True)

    def __str__(self):
        return f'{self.user}_{self.task}'

    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
