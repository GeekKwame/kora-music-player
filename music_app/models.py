from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_avatar_url(self):
        if self.avatar:
            try:
                return self.avatar.url
            except Exception:
                pass
        if self.avatar_url:
            return self.avatar_url
        return None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def _get_user_avatar(self):
    try:
        profile = Profile.objects.filter(user=self).first()
        if profile:
            return profile.get_avatar_url()
    except Exception:
        pass
    return None


# Attach convenience property to User so {{ request.user.avatar_url }} always works
User.add_to_class('avatar_url', property(_get_user_avatar))
