# -*- coding:utf-8 -*-
from django.views.generic import CreateView, ListView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from .models import Talk
from .forms import TalkForm, VoteForm
from .utils import token_required


class SubmissionView(CreateView):
    form_class = TalkForm
    template_name = 'submission/submission.html'
    model = Talk
    success_url = lazy(reverse, str)('submission:submission')

    def form_valid(self, form):
        response = super(SubmissionView, self).form_valid(form)
        messages.success(self.request, _(u'Palestra submetida com sucesso!'))
        return response


class SubmissionListView(ListView):
    model = Talk
    template_name = 'submission/vote.html'
    context_object_name = 'talks'
    paginate_by = 1

    @method_decorator(token_required)
    def dispatch(self, *args, **kwargs):
        return super(SubmissionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Talk.objects.filter(type__in=['talk', 'tutorial'])

    def post(self, request):

        form = VoteForm(request.POST)
        if form.is_valid():
            form.save(request.session['email'])

        page = request.POST.get('page', None)
        if page is None:
            return redirect('submission:success')
        return redirect(reverse('submission:vote') + '?page={0}'.format(page))
