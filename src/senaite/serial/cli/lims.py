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

import re

import requests

from . import logger

# SENAITE.JSONAPI route
API_BASE_URL = "@@API/senaite/v1"


class Session(object):

    def __init__(self, url, username, password):
        self.url = url
        self.session = None
        self.username = username
        self.password = password

    def auth(self):
        logger.info("Starting session with SENAITE ...")
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

        # try to get the version of the remote JSON API
        version = self.get("version")
        if not version or not version.get("version"):
            logger.error("senaite.jsonapi not found on at {}".format(self.url))
            return False

        # try to get the current logged in user
        user = self.get("users/current")
        user = user.get("items", [{}])[0]
        if not user or user.get("authenticated") is False:
            logger.error("Wrong username/password")
            return False

        logger.info("Session established ('{}') with '{}'"
                    .format(self.username, self.url))
        return True

    def post(self, endpoint, payload):
        """Sends a POST request to SENAITE
        """
        url = self.get_url(endpoint)
        try:
            response = self.session.post(url, data=payload)
        except Exception as e:
            message = "Could not send POST to {}".format(url)
            logger.error(message)
            logger.error(e)
            return {}

        return response.json()

    def get(self, endpoint, timeout=60):
        """Fetch the given url or endpoint and return a parsed JSON object
        """
        url = self.get_url(endpoint)
        try:
            response = self.session.get(url, timeout=timeout)
        except Exception as e:
            message = "Could not connect to {}".format(url)
            logger.error(message)
            logger.error(e)
            return {}

        status = response.status_code
        if status != 200:
            message = "GET for {} returned {}".format(endpoint, status)
            logger.error(message)
            return {}

        return response.json()

    def get_url(self, endpoint):
        """Create an API URL from an endpoint or absolute url
        """
        return "{}/{}/{}".format(self.url, API_BASE_URL, endpoint)


def get_senaite_connection_info(url):
    """Returns a dict with the connection information (url, user, password)
    """
    def get_schema(url):
        sch = url.split("://")
        if not sch:
            raise ValueError("schema is missing (http/https)")
        elif sch[0].lower() not in ["http", "https"]:
            raise ValueError("not valid schema: {}".format(sch))
        return sch[0].lower()

    def get_user_password(url):
        tokens = url.split("://")
        if len(tokens) != 2:
            raise ValueError("malformed url")
        user_pass = tokens[1].split("@") or [""]
        user_pass = map(lambda s: s.strip(), user_pass[0].split(":"))
        user_pass = filter(None, user_pass)
        if not user_pass or len(user_pass) < 2:
            raise ValueError("missing user:password")
        elif len(user_pass) > 2:
            raise ValueError("malformed user:password")
        return user_pass[0], user_pass[1]

    def get_senaite_url(url):
        tokens = url.split("://")
        if len(tokens) != 2:
            raise ValueError("malformed url")
        senaite_url = tokens[1].split("@")
        if not senaite_url:
            raise ValueError("missing url")
        elif len(senaite_url) != 2:
            raise ValueError("malformed url")
        schema = get_schema(url)
        senaite_url = "{}://{}".format(schema, senaite_url[1])
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        if re.match(pattern, senaite_url):
            return senaite_url
        else:
            ValueError("malformed url")

    # Get user and password
    user, password = get_user_password(url)

    # Get the url
    url = get_senaite_url(url)

    # Try to connect
    logger.info("Trying connection with {} ...".format(url))
    session = Session(url, user, password)
    if not session.auth():
        raise ValueError("Cannot connect to {} ".format(url))

    return dict(url=url, user=user, password=password)
