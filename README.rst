Serial client for SENAITE
=========================

.. image:: https://img.shields.io/pypi/v/senaite.serial.cli.svg?style=flat-square
    :target: https://pypi.python.org/pypi/senaite.serial.cli

.. image:: https://readthedocs.org/projects/pip/badge/
    :target: https://senaiteserialcli.readthedocs.org

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.serial.cli.svg?style=flat-square
    :target: https://github.com/senaite/senaite.serial.cli/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.serial.cli.svg?style=flat-square
    :target: https://github.com/senaite/senaite.serial.cli/issues

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
-----

This package provides a command line interface to connect through RS-232 with
devices that are compliant with the `ASTM-E1381-95`_ standard for the
transmission of messages between systems.

This command line tool works together with `senaite.serial`_, an add-on that
enables the reception of ASTM-like messages for `SENAITE LIMS`_.


.. code-block:: shell

    $ senaite_serial -h
    usage: senaite_serial [-h] [-v] [-b BAUDRATE] [-u URL] [-r RETRIES] [-d DELAY]
                          [-t]
                          port

    SENAITE Serial client interface

    positional arguments:
      port                  COM Port to connect. Serial client will listen to this
                            port for incoming data and use this same port to send
                            data back

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Verbose logging (default: False)
      -b BAUDRATE, --baudrate BAUDRATE
                            Baudrate (default: 9600)
      -u URL, --url URL     SENAITE full URL address, with username and password:
                            'http(s)://<user>:<password>@<senaite_url>'. (default:
                            None)
      -r RETRIES, --retries RETRIES
                            Number of attempts of reconnection when SENAITE
                            instance is not reachable. Only has effect when
                            argument --url is set (default: 3)
      -d DELAY, --delay DELAY
                            Time delay in seconds between retries when SENAITE
                            instance is not reachable. Only has effect when
                            argument --url is set (default: 5)
      -t, --dry-run         Dry run. Data won't be sent to SENAITE instance. This
                            argument only has effect when argument --url is set
                            (default: False)


Documentation
-------------

* https://senaiteserialcli.readthedocs.io


Feedback and support
--------------------

* `Community site`_
* `Gitter channel`_
* `Users list`_


License
-------

**SENAITE.SERIAL.CLI** Copyright (C) 2020 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2`_ as published by the
Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

.. Links

.. _ASTM-E1381-95: https://www.astm.org/DATABASE.CART/HISTORICAL/E1381-95.htm
.. _senaite.serial: https://pypi.python.org/pypi/senaite.serial
.. _SENAITE LIMS: https://www.senaite.com
.. _Community site: https://community.senaite.org/
.. _Gitter channel: https://gitter.im/senaite/Lobby
.. _Users list: https://sourceforge.net/projects/senaite/lists/senaite-users
.. _GNU General Public License version 2: https://github.com/senaite/senaite.serial.cli/blob/master/LICENSE