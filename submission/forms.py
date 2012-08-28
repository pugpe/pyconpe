# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Talk


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        print 'ok'
        for field in self.fields:
            self.fields[field].label = u''

        self.fields['name'].initial = _(u'Digite seu nome')
        self.fields['email'].initial = _(u'Digite seu E-mail')
        self.fields['phone'].initial = _(u'Telefone para contato')
        self.fields['macro_theme'].initial = _(u'MacroTema')
        self.fields['title'].initial = _(u'Título')

        levels = (('', u'Nível de Palestra'),) + Talk.LEVELS
        self.fields['level'].widget.choices = levels

        self.fields['type'].widget.choices = (('' , u'Tipo'),) + Talk.TYPES

        types = (('' , u'Já Palestrou em algum encontro PUG-PE'),) + Talk.BOOL
        self.fields['talk_once'].widget.choices = types

        self.fields['summary'].initial = _(u'Digite o resumo da sua palestra ou tutorial')
