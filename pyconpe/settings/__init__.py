# -*- coding:utf-8 -*-
import socket
from pyconpe.settings.base import *

HOSTNAME = socket.gethostname()
if HOSTNAME == 'pyconpe':
    from pyconpe.settings.prod import *
else:
    try:
        from pyconpe.settings.local import *
    except:
        pass
