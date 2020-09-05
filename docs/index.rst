senaite.serial.cli
==================

This package provides a command line for interfacing systems to SENAITE LIMS
across the serial RS-232 communications port.

This interface is compliant with the industry supported standard CLSI
(`Clinical and Laboratory Standards Institute`_, formerly NCCLS) `LIS1-A`_
*"Specification for Low-Level Protocol to Transfer Messages Between Clinical
Laboratory Instruments and Computer Systems"*, a revision of `ASTM E1381-02`_.

However, this tool is meant to be generic enough so it can be extended with
other communication protocols and standards.

.. note:: In 2001, `ASTM Committee E31`_ decided to restructure its operations,
   with the intent of focusing on standards-development issues such as security,
   privacy, and the electronic health record. Part of the reorganization plan
   was to transfer responsibility for E31.13 standards to NCCLS. Following this
   transfer, standard ASTM E1381 was redesignated as NCCLS standards LIS1.

This command line tool works together with `senaite.lis2a`_, an add-on that
enables the reception and interpretation of CLSI `LIS2-A2`_ messages for
`SENAITE LIMS`_.


Table of Contents:

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   testing
   examples


.. Links

.. _Clinical and Laboratory Standards Institute: https://clsi.org
.. _LIS1-A: https://clsi.org/standards/products/automation-and-informatics/documents/lis01/
.. _LIS2-A2: https://clsi.org/standards/products/automation-and-informatics/documents/lis02/
.. _ASTM E1381-02: https://www.astm.org/Standards/E1381.htm
.. _ASTM E1394-97: https://www.astm.org/Standards/E1394.htm
.. _ASTM Committee E31: https://www.astm.org/COMMITTEE/E31.htm
.. _senaite.lis2a: https://pypi.python.org/pypi/senaite.lis2a2
.. _SENAITE LIMS: https://www.senaite.com

