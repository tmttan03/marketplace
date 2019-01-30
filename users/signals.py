import stripe

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, userStripe

stripe.api_key = "sk_test_LWtBD1TOvlfIMzdIawpJvHzj"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


@receiver(post_save, sender=User)
def stripeCallback(sender, instance, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=instance)
    if created:
        print(f'{instance.username} Stripe')
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=instance.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()


@receiver(post_save, sender=User)
def profileCallback(sender, instance, **kwargs):
    userProfile, is_created = Profile.objects.get_or_create(user=instance)
    if is_created:
        userProfile.name = user.username
        userProfile.save()
