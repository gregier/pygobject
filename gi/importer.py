# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2005-2009 Johan Dahlin <johan@gnome.org>
#
#   importer.py: dynamic importer for introspected libraries.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import sys

from .repository import repository
from .module import DynamicModule

class DynamicImporter(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @staticmethod
    def find_module(name, path=None):
        if name == 'cairo':
            return None
        namespace = repository.require(name)
        if namespace:
            return DynamicImporter(name, path)

    def load_module(self, name):
        module = repository.get_module(name)
        if module is not None:
            return module

        module_name = 'gi.overrides.%s' % (name,)
        try:
            module = __import__(module_name, {}, {}, ['%sModule' % (name,)])
            modtype = getattr(module, name + 'Module')
        except ImportError, e:
            modtype = DynamicModule
        return modtype(name, self.path)


def install_importhook():
    sys.meta_path.append(DynamicImporter)
