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

This package provides a command line for interfacing systems to SENAITE LIMS
across the serial RS-232 communications port.

This interface is compliant with the industry supported standard CLSI
(`Clinical and Laboratory Standards Institute`_, formerly NCCLS) `LIS1-A`_
*"Specification for Low-Level Protocol to Transfer Messages Between Clinical
Laboratory Instruments and Computer Systems"*, a revision of `ASTM E1381-02`_.

However, this tool is meant to be generic enough so it can be extended with
other communication protocols and standards.

This command line tool works together with `senaite.lis2a`_, an add-on that
enables the reception and interpretation of CLSI `LIS2-A2`_ messages for
`SENAITE LIMS`_.


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

.. _Clinical and Laboratory Standards Institute: https://clsi.org
.. _LIS1-A: https://clsi.org/standards/products/automation-and-informatics/documents/lis01/
.. _LIS2-A2: https://clsi.org/standards/products/automation-and-informatics/documents/lis02/
.. _ASTM E1381-02: https://www.astm.org/Standards/E1381.htm
.. _ASTM E1394-97: https://www.astm.org/Standards/E1394.htm
.. _ASTM Committee E31: https://www.astm.org/COMMITTEE/E31.htm
.. _senaite.lis2a: https://pypi.python.org/pypi/senaite.lis2a
.. _SENAITE LIMS: https://www.senaite.com
.. _Community site: https://community.senaite.org/
.. _Gitter channel: https://gitter.im/senaite/Lobby
.. _Users list: https://sourceforge.net/projects/senaite/lists/senaite-users
.. _GNU General Public License version 2: https://github.com/senaite/senaite.serial.cli/blob/master/LICENSE