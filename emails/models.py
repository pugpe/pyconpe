from django.db import models
from django.utils.translation import ugettext_lazy as _


class Email(models.Model):
    email = models.EmailField(u'E-mail', max_length=254, unique=True)
    opt_in = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email
