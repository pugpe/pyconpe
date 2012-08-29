# -*- coding:utf-8 -*-
import os

from fabric.api import run, env, cd, put, sudo
from fabric.contrib.files import upload_template, exists
from fabric.contrib.project import rsync_project
from fabric.context_managers import prefix, settings

from provyfile import servers


def uptime():
    run("uptime")


def prod():
    env.user = servers['frontend']['user']
    env.hosts=[servers['frontend']['address']]

    env.project_root = os.path.dirname(os.path.abspath(__file__))
    env.opts = servers['frontend']['options']

    ve = '/home/{0}/.virtualenvs/{1}/'.format(env.user, env.opts['site'])
    env.opts.update({
        'virtualenv': ve,
        'python': os.path.join(ve, 'bin/python'),
        'local_settings': os.path.dirname(os.path.abspath(__file__)),
        'user': env.user,
    })


def setup_env():
    site = env.opts['site']

    if not exists('/home/{0}/.virtualenvs/{1}'.format(env.user, site)):
        with settings(warn_only=True):
            run('mkdir .virtualenvs')
        run('virtualenv .virtualenvs/{0} --no-site-packages'.format(site))


def update_supervisord():
    '''Place supervisord conf files of project programs'''
    include_path = env.opts['include_dir']

    template_dir = os.path.join(env.project_root, 'files')
    kwargs = {'context': env.opts, 'use_jinja': True,
              'template_dir': template_dir, 'use_sudo': True}

    upload_template('supervisor_gunicorn.conf', include_path, **kwargs)


def rsync():
    rsync_project(
        '/srv', os.path.abspath('../../'), delete=True,
         exclude=['*.pyc', '*.sqlite', 'uploads', '*.swp', 'prod.py', '*.dat',
                  '*.dat.gz'],
    )


def collect_static():
    with prefix('source {0}bin/activate'.format(env.opts['virtualenv'])):
        with cd(env.opts['project_path']):
            run('python manage.py collectstatic --noinput')


def install_deps():
    with prefix('source {0}bin/activate'.format(env.opts['virtualenv'])):
        with cd(env.opts['project_path']):
            run('pip install -r requirements.txt')



def run_tests():
    with prefix('source {0}bin/activate'.format(env.opts['virtualenv'])):
        with cd(env.opts['project_path']):
            run('python manage.py test')


def migrate():
    with prefix('source {0}bin/activate'.format(env.opts['virtualenv'])):
        with cd(env.opts['project_path']):
            run('python manage.py syncdb --noinput')
            run('python manage.py migrate')


def translate():
    with prefix('source {0}bin/activate'.format(env.opts['virtualenv'])):
        with cd(env.opts['project_path']):
            run('django-admin.py compilemessages')


def restart_supervisord():
    sudo('service supervisord restart')


def supervisor_status():
    sudo('supervisorctl status')


def deploy():
    setup_env()
    update_supervisord()
    rsync()
    install_deps()
    collect_static()
    #run_tests()
    migrate()
    restart_supervisord()
