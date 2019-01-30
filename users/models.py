from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
    	super().save()
    	img = Image.open(self.image.path)
    	if img.height > 300 or img.width > 300:
    		output_size = (300,300)
    		img.thumbnail(output_size)
    		img.save(self.image.path)


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Stripe Account'

    def __unicode__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username


