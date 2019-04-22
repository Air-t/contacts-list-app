from django.db import models
from PIL import Image


PHONE_CHOICES = (
    (0, 'Mobile'),
    (1, 'Home'),
    (2, 'Work'),
    (3, 'Private'),
    (4, 'FAX'),
)

EMAIL_CHOICES = (
    (0, 'Mobile'),
    (1, 'Home'),
    (2, 'Private'),
)


class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='avatar', blank=True, default='default.png')

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self):
        super().save()

        # todo rename saved files
        img = Image.open(self.photo.path)
        if img.height > 128 or img.width > 128:
            output_size = (128, 128)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"


class Address(models.Model):
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    home_no = models.CharField(max_length=64)
    apartment_no = models.CharField(max_length=64)
    zip_code = models.IntegerField(blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}, {self.street} street, " \
               f"{self.home_no}/{self.apartment_no}"


class Phone(models.Model):
    number = models.CharField(max_length=32)
    number_type = models.IntegerField(default=0, choices=PHONE_CHOICES)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number} {self.number_type}"


class Email(models.Model):
    email = models.CharField(max_length=64)
    email_type = models.IntegerField(default=0, choices=EMAIL_CHOICES)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} {self.email_type}"


class Group(models.Model):
    name = models.CharField(max_length=128, unique=True)
    person = models.ManyToManyField(Person)

    def __str__(self):
        return self.name
