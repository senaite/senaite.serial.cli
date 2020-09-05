Examples
========

Example 1
---------

Input:

.. literalinclude:: examples/example1

Output:

.. code-block::shell

    $ senaite_serial /dev/pts/7
    Listening on port /dev/pts/7, press Ctrl+c to exit.

    * Establishment Phase completed
    * Transfer Phase started ...
    Frame 1 received
    Frame 2 received
    Frame 3 received
    Frame 4 received
    Frame 5 received
    Frame 6 received
    Frame 7 received
    * Transfer Phase completed
    --------------------------------------------------------------------------------
    H|\^&|||ALCZC12033KD^Roche^AMPLILINK^3.3.7.1201^Roche ASTM+^CZC12033KD^169.254.218.147||||||||1|20190822160121
    P|1
    O|1|BP19-24277|BP19-24277|^^^ALL||20190819215010|||||A
    R|1|^^^HI2CAP96|61|cp/mL|20^10000000^TiterRanges|N||V||BVURE|20190820092419|20190820122902|Cobas TaqMan
    C|1||Accepted|G
    C|2|I|TM40^ STEP_CORR-2|I
    L|1|N
    --------------------------------------------------------------------------------
    * Entering Neutral state



