# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.SERIAL.CLI.
#
# SENAITE.SERIAL.CLI is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020 by it's authors.
# Some rights reserved, see README and LICENSE.


class MessageHandler(object):

    def __init__(self, **kwargs):
        pass

    def write(self, command):
        raise NotImplementedError("write is not implemented")

    def read(self):
        raise NotImplementedError("read is not implemented")

    def is_timeout(self):
        raise NotImplementedError("is_timeout is not implemented")

    def reset(self):
        raise NotImplementedError("reset is not implemented")
