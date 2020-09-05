Testing
=======

It is possible to use `socat` to create a pair of virtual serial ports:

.. code-block:: shell

    $ socat -d -d pty,raw,echo=0 pty,raw,echo=0
    2019/05/02 17:26:21 socat[24050] N PTY is /dev/ttys002
    2019/05/02 17:26:21 socat[24050] N PTY is /dev/ttys007

In this example, two serial ports `ttys002` and `ttys007` were created.

Now we can start the command tool listening on one serial port:

.. code-block:: shell

    $ serial -v /dev/ttys007
    Listening on port /dev/ttys007, press Ctrl+c to exit.

And send messages to the other port:

.. code-block:: shell

    $ echo "H|Hello|Serial|Port|\nL|1" > /dev/ttys002


Send messages from a file
-------------------------

If you have a file with the data to be transmitted, you can make use of `sed` to
read and send the contents of the file line by line. Create a bash script file
"send" first, like follows:

.. code-block:: bash

    #!/bin/bash
    echo -n -e `sed -n $3p $1` > $2

Give execution permissions:

.. code-block:: shell

    $ chmod +x send

Having a file "input.txt", you can send the contents of this file sequentially,
by executing the following command:

.. code-block:: shell

    $ send input.txt /dev/ttys002 1

Where the last number represents the line number from the input file to send.


Escape characters
-----------------

.. code-block::

    001   1     01    SOH (start of heading) \x01
    002   2     02    STX (start of text)
    003   3     03    ETX (end of text)
    004   4     04    EOT (end of transmission)
    005   5     05    ENQ (enquiry)
    006   6     06    ACK (acknowledge)
    007   7     07    BEL '\a' (bell)
    010   8     08    BS  '\b' (backspace)
    011   9     09    HT  '\t' (horizontal tab)
    012   10    0A    LF  '\n' (new line)
    013   11    0B    VT  '\v' (vertical tab)
    014   12    0C    FF  '\f' (form feed)
    015   13    0D    CR  '\r' (carriage ret)
    016   14    0E    SO  (shift out)
    017   15    0F    SI  (shift in)
    020   16    10    DLE (data link escape)
    021   17    11    DC1 (device control 1)
    022   18    12    DC2 (device control 2)
    023   19    13    DC3 (device control 3)
    024   20    14    DC4 (device control 4)
    025   21    15    NAK (negative ack.)
    026   22    16    SYN (synchronous idle)
    027   23    17    ETB (end of trans. blk)
    030   24    18    CAN (cancel)
    031   25    19    EM  (end of medium)
    032   26    1A    SUB (substitute)
    033   27    1B    ESC (escape)
    034   28    1C    FS  (file separator)
    035   29    1D    GS  (group separator)
    036   30    1E    RS  (record separator)
    037   31    1F    US  (unit separator)
