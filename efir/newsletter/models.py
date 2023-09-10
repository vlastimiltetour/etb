from django.db import models

# Create your models here.


class Newsletter(models.Model):
    email = models.CharField(max_length=50, verbose_name="Email", editable=False)
    saved_when = models.DateTimeField(auto_now_add=True, verbose_name="Přihlášeno", editable=False)
    active = models.BooleanField(default=True)

 