# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Talk, Vote


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = u''

        self.fields['name'].initial = _(u'Digite seu nome')
        self.fields['email'].initial = _(u'Digite seu E-mail')
        self.fields['phone'].initial = _(u'Telefone para contato')
        self.fields['title'].initial = _(u'Título')

        levels = (('', u'Nível de Palestra'),) + Talk.LEVELS
        self.fields['level'].widget.choices = levels

        self.fields['type'].widget.choices = (('' , u'Tipo'),) + Talk.TYPES[2:]

        types = (('' , u'Já Palestrou em algum encontro PUG-PE'),) + Talk.BOOL
        self.fields['talk_once'].initial = u''
        self.fields['talk_once'].widget.choices = types
        self.fields['talk_once'].required = True

        themes = (('', _(u'Qual é o macro-tema da sua palestra ?')),)
        self.fields['macro_theme'].widget.choices = themes + Talk.THEMES

        self.fields['summary'].initial = _(u'Digite o resumo da sua palestra '
                                           u'ou tutorial')


class VoteForm(forms.Form):
    talk = forms.Field(widget=forms.HiddenInput)
    type = forms.Field(widget=forms.HiddenInput)

    def save(self, email):
        talk = self.cleaned_data['talk']
        talk = Talk.objects.get(pk=talk)
        type = self.cleaned_data['type']

        v = Vote.objects.get_or_create(email=email, talk=talk)[0]
        if v.type != type:
            v.type = type
            v.save()

        return v
