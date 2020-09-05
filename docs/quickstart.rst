Quickstart
==========

Check the --help from senaite.serial.cli with:

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