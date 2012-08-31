#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os.path import join

from fabric.context_managers import settings

from provy.core import Role, AskFor
from provy.more.centos import YumRole, UserRole, PipRole
from provy.more.centos import HostNameRole, RabbitMqRole

from centos import NginxRole, SupervisorRole, MemcachedRole, MySQLRole


class PreSetupRole(Role):
    def provision(self):
        new_user = self.context['new_user']

        self.execute('yum install -y sudo', stdout=False, sudo=True)

        with self.using(UserRole) as role:
            role.ensure_group('admin')
            self.ensure_line('%admin  ALL=(ALL) NOPASSWD: ALL', '/etc/sudoers',
                             sudo=True)
            role.ensure_user(new_user, is_admin=True)

        # TODO: Melhorar
        self.ensure_dir('/home/{0}/.ssh/'.format(new_user), owner=new_user)
        self.change_dir_mode('/home/{0}/.ssh/'.format(new_user), 700)

        authorized_keys = '/home/{0}/.ssh/authorized_keys'.format(new_user)

        cmd = 'cat /root/.ssh/authorized_keys >> {0}'.format(authorized_keys)
        self.execute(cmd, sudo=True)

        self.change_file_owner(authorized_keys, new_user)
        self.change_file_mode(authorized_keys, 600)
        # TODO: Disable root login


class MainServer(Role):
    def provision(self):
        with self.using(HostNameRole) as role:
            role.ensure_hostname(self.context['site'])

        with settings(warn_only=True):
            self.execute('rpm -Uvh http://download.fedoraproject.org/pub/epel/'
                         '6/i386/epel-release-6-7.noarch.rpm', sudo=True)

        self.log('Starting NginxRole')
        with self.using(NginxRole) as role:
            role.ensure_conf(conf_template='nginx.conf')
            role.ensure_site_disabled('default')

            role.create_site(
                site=self.context['site'],
                template=self.context['template'],
            )
            role.ensure_site_enabled(self.context['site'])

        self.log('Starting MemcachedRole')
        self.provision_role(MemcachedRole)

        self.log('Starting SupervisorRole')
        with self.using(SupervisorRole) as role:
            self.ensure_dir('/var/log/supervisor', sudo=True)
            self.ensure_dir(self.context['include_dir'], sudo=True)

            role.config(
                config_file_directory='/etc/',
                log_folder='/var/log/supervisor',
                user='root',
            )
            include = self.context['include']
            # Should config have kwargs?
            role.context['supervisor-config']['include'] = include
            role.restart()

        self.log('Running Rsync')
        with self.using(YumRole) as role:
            role.ensure_package_installed('rsync')

        self.ensure_dir(
            self.context['project_path'], owner=self.context['owner'],
            sudo=True,
        )

        from fabfile import rsync
        rsync()
        # Todo: Melhorar
        # Place prod.py settings in right path
        self.update_file(
            'prod.py',
            join(self.context['project_path'], 'pyconpe/settings/prod.py'),
            options=self.context,
        )


        self.log('Configuring static dir')
        self.ensure_dir('/srv/static', owner=self.context['owner'], sudo=True)
        self.ensure_dir('/srv/media', owner=self.context['owner'], sudo=True)
        self.execute('chmod +x /srv', sudo=True)

        self.log('Starting Virtualenv')
        with self.using(PipRole) as role:
            role.ensure_package_installed('virtualenv')

        self.log('Starting deps')
        with self.using(YumRole) as role:
            # Deps for PIL
            role.ensure_package_installed('zlib-devel')
            role.ensure_package_installed('libjpeg-devel')
            role.ensure_package_installed('freetype-devel')

            # gettext
            role.ensure_package_installed('gettext')

            # wget
            role.ensure_package_installed('GeoIP')
            role.ensure_package_installed('wget')

            role.ensure_package_installed('subversion')
            role.ensure_package_installed('git')


address = '174.129.42.92'

servers = {
    'pre_setup': {
        'address': address,
        'user': 'root',
        'roles': [
            PreSetupRole,
        ],
        'options': {
            'new_user': 'pyconpe',
        }
    },

    'frontend': {
        'address': address,
        'user': 'pyconpe',
        'roles': [
            MainServer
        ],
        'options': {
            # Smtp
            'smtp_user': 'AKIAICFVIQFBN77PTE7Q' ,
            'smtp_password' '':
                AskFor('smtp', 'Please enter smtp password'),
            # supervisord
            'include_dir': '/etc/supervisor/conf.d/',
            'include': '/etc/supervisor/conf.d/*.conf',

            # Project specific
            'site': 'pyconpe',
            'template': 'pyconpe',

            'project_path': '/srv/pyconpe/',
        }
    }
}
