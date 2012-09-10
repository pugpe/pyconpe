from submission.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def results(request):
    ctx = {}
    talk_list = []
    talks = Talk.objects.all()
    for t in talks:
        talk = {}
        talk['likes'] =  t.vote_set.filter(type='like').count()
        talk['dislikes'] =  t.vote_set.filter(type='dislike').count()
        talk['name'] = t.name
        talk_list.append(talk)
    ctx['talks'] = sorted(talk_list, key=lambda x:x['likes'], reverse=True)
    return render(request, 'core/results.html', ctx)