from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from LoveForLive.settings import MEDIA_ROOT
from PIL import Image
from django.core.validators import FileExtensionValidator


class RequestConsultation(models.Model):
    name = models.CharField('Имя Фамилия', max_length=50)
    age = models.IntegerField('Возраст')
    email = models.EmailField('Почта отправителя')
    phone = PhoneNumberField('Номер телефона', blank=True)
    country = models.CharField('Страна проживания', max_length=50)
    date = models.DateTimeField('Дата запроса', default=timezone.now)
    pay_status = models.BooleanField('Статус оплаты', default=False)
    payment_id = models.CharField('ID платежа', default='0', max_length=100)
    pay_sum = models.IntegerField('Оплачено', default=0)
    agreement = models.BooleanField('Согласие с договором', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запрос на консультацию'
        verbose_name_plural = 'Запросы на консультацию'


class Articles(models.Model):
    title = models.CharField('Заголовок статьи', max_length=50)
    text = models.TextField('Текст статьи')
    img = models.ImageField('Изображение статьи', default='default.png', upload_to='articles')
    date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        try:
            this = Articles.objects.get(id=self.id)
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

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Articles, self).delete(*args, **kwargs)
        if path != MEDIA_ROOT + '\default.png':
            storage.delete(path)

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'


class Receipts(models.Model):
    title = models.CharField('Заголовок рецепта', max_length=100)
    text = models.TextField('Текст рецепта')
    img = models.ImageField('Изображение рецепта', default='default.png', upload_to='receipts')
    date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('receipt-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        try:
            this = Receipts.objects.get(id=self.id)
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

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Receipts, self).delete(*args, **kwargs)
        if path != MEDIA_ROOT + '\default.png':
            storage.delete(path)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class HomeVideo(models.Model):
    title = models.CharField('Заголовок видео', max_length=100)
    video = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        default=None
    )
    poster = models.ImageField("Постер для видео", upload_to='posters', default='poster.jpg')

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.poster.path)
        if image.height > 1000 or image.width > 600:
            resize = (1000, 600)
            image.thumbnail(resize)
            image.save(self.poster.path)