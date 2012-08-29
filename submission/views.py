# -*- coding:utf-8 -*-
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy 

from .models import Talk
from .forms import TalkForm


class SubmissionView(CreateView):
    form_class = TalkForm
    template_name = 'submission/submission.html'
    model = Talk
    success_url = lazy(reverse, str)('submission:submission')

    def form_valid(self, form):
        response = super(SubmissionView, self).form_valid(form)
        messages.success(self.request, _(u'Palestra submetida com sucesso!'))
        return response
