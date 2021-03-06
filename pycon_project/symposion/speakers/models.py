import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from markitup.fields import MarkupField


class Speaker(models.Model):
    
    SESSION_COUNT_CHOICES = [
        (1, _("One session")),
        (2, _("Two session"))
    ]
    
    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(_("Name"), max_length=100)
    biography = MarkupField(_("Biography"), help_text=_("A little bit about you. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."))
    photo = models.ImageField(_("Photo"), upload_to="speaker_photos", blank=True, help_text=_('Please upload JPG with 950x1190 dimension above'))
    twitter_username = models.CharField(
        _("Twitter username"),
        max_length = 15,
        blank = True,
        help_text = _("Your Twitter account, with or without the @")
    )
    annotation = models.TextField() # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    release_permission = models.BooleanField(_("Release permission"), help_text=_('I agree PyCon TW can release my slides and video recording.'))
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    sessions_preference = models.IntegerField(
        _("Sessions preference"),
        choices=SESSION_COUNT_CHOICES,
        null=True,
        blank=True,
        help_text=_("If you've submitted multiple proposals, please let us know if you only want to give one or if you'd like to give two talks.")
    )
    
    def __unicode__(self):
        if self.user:
            return self.name
        else:
            return "?"
    
    def get_absolute_url(self):
        return reverse("speaker_edit")
    
    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email
