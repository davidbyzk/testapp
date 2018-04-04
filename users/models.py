from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
import hashlib

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from allauth.account.signals import user_signed_up





class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
"""
    def guess_display_name(self):
       # Set a display name, if one isn't already set.
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])  # like "Andrew E"
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'You'
        self.display_name = dn.strip()
"""
class UserProfile(models.Model):
    """Profile data about a user.
    Certain data makes sense to be in the User model itself, but some
    is more "profile" data than "user" data. I think this is things like
    date-of-birth, favourite colour, etc. If you have domain-specific
    profile information you might create additional profile classes, like
    say UserGeologistProfile.
    """
    user = models.OneToOneField(CustomUser, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)

    # I oscillate between whether the ``avatar_url`` should be
    # a) in the User model
    # b) in this UserProfile model
    # c) in a table of it's own to track multiple pictures, with the
    #    "current" avatar as a foreign key in User or UserProfile.
    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    dob = models.DateField(verbose_name="dob", blank=True, null=True)

    public_token = models.CharField(max_length=100, blank=True, null=True, verbose_name='public_token')
    access_token = models.CharField(max_length=100, blank=True, null=True, verbose_name='access_token')
    item_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='item_ID')

    def __str__(self):
        return force_text(self.user)

    class Meta():
        db_table = 'user_profile'

@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    preferred_avatar_size_pixels = 256

    picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
        preferred_avatar_size_pixels
    )

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            user.first_name = name.split()[0]
            user.last_name = name.split()[1]

        if sociallogin.account.provider == 'facebook':
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']
            # verified = sociallogin.account.extra_data['verified']
            picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                sociallogin.account.uid, preferred_avatar_size_pixels)

        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']
            # verified = sociallogin.account.extra_data['verified_email']
            picture_url = sociallogin.account.extra_data['picture']

    profile = UserProfile(user=user, avatar_url=picture_url)
    profile.save()

    #user.guess_display_name()
    user.save()
