from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from courses.models import Courses, Allowance, Tasks, LessonProgress


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField('Номер телефона', blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        courses = Courses.objects.all()
        tasks = Tasks.objects.all()
        for course in courses:
            Allowance(user=self.user, course=course, allow=False).save()
        for task in tasks:
            LessonProgress(user=self.user, task=task).save()

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
