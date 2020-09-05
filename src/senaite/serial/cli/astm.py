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

import threading
import time

import lims
from . import logger
from .handler import MessageHandler

#: Message start token.
STX = b'\x02'
#: Message end token.
ETX = b'\x03'
#: ASTM session termination token.
EOT = b'\x04'
#: ASTM session initialization token.
ENQ = b'\x05'
#: Command accepted token.
ACK = b'\x06'
#: Command rejected token.
NAK = b'\x15'
#: Message chunk end token.
ETB = b'\x17'
LF  = b'\x0A'
CR  = b'\x0D'
#: CR + LF shortcut.
CRLF = CR + LF

MAPPINGS = {
    STX: "<STX>",
    ETX: "<ETX>",
    EOT: "<EOT>",
    ENQ: "<ENQ>",
    ACK: "<ACK>",
    NAK: "<NAK>",
    ETB: "<ETB>",
    LF: "<LF>",
    CR: "<CR>",
    CRLF: "<CR><LF>"
}


class Message(object):
    """A collection of related information on a single topic, used here to mean
    all the identity, tests, and comments sent at one time. When used with
    Specification E 1394, this term means a record as defined by Specification
    E 1394. Messages are sent in frames, each frame contains a maximum of 247
    characters (including frame overhead). Messages longer than 240 characters
    are divided between two or more frames.
    """

    frames = None

    def __init__(self, start_fn=1):
        self.frames = []
        self.start_fn = start_fn

    def add_frame(self, frame):
        """Tries to add a frame into the current message
        """
        if self.can_add_frame(frame):
            self.frames.append(frame)

    def can_add_frame(self, frame):
        """A frame should be rejected because:
        (1) Any character errors are detected (parity error, framing
            error, etc.),
        (2) The frame checksum does not match the checksum computed on the
            received frame,
        (3) The frame number is not the same as the last accepted frame or one
            number higher (modulo 8).
        """
        if not frame.is_valid():
            return False
        elif frame.fn != (len(self.frames) + self.start_fn) % 8:
            logger.info("No valid frame: FN is not consecutive")
            return False
        elif self.is_complete():
            logger.info("No valid frame: Message is complete")
            return False
        return True

    def is_complete(self):
        """Returns whether the current message is complete
        """
        if self.is_empty():
            return False
        return self.frames[-1].is_final

    def is_empty(self):
        """Returns whether this message is empty
        """
        return not self.frames

    def text(self):
        """Text representation of the message
        """
        texts = map(lambda frame: frame.text, self.frames)
        return CRLF.join(texts)


class Frame(object):
    """A subdivision of a message, used to allow periodic communication
    housekeeping such as error checks and acknowledgements. A frame contains a
    maximum of 247 characters (including frame overhead)
    """
    frame = None

    def __init__(self, frame):
        """
        The frame structure is illustrated as follows:
            <STX> FN text <ETB> C1 C2 <CR> <LF>  intermediate frame
            <STX> FN text <ETX> C1 C2 <CR> <LF>  end frame
        where:
            <STX> Start of Text transmission control character
            FN    single digit Frame Number 0 to 7
            text  Data Content of Message
            <ETB> End of Transmission Block transmission control character
            <ETX> 5 End of Text transmission control character
            C1    5 most significant character of checksum 0 to 9 and A to F
            C2    5 least significant character of checksum 0 to 9 and A to F
            <CR> 5 Carriage Return ASCII character
            <LF> 5 Line Feed ASCII character

        Any characters occurring before the <STX> or after the end of the
        block character (the <ETB> or <ETX>) are ignored by the receiver when
        checking the frame.
        """
        if STX in frame:
            self.frame = frame[frame.index(STX):]

    @property
    def fn(self):
        """Frame Number: The frame number permits the receiver to distinguish
        between new and retransmitted frames. It is a single digit sent
        immediately after the <STX> character.
        The frame number is an ASCII digit ranging from 0 to 7. The frame number
        begins at 1 with the first frame of the Transfer phase. The frame number
        is incremented by one for every new frame transmitted. After 7, the
        frame number rolls over to 0, and continues in this fashion.
        """
        return int(self.frame[1])

    @property
    def text(self):
        """Data content of the frame
        """
        end = self.is_intermediate and ETB or ETX
        return self.frame[2:self.frame.index(end)]

    @property
    def is_intermediate(self):
        """A message containing more than 240 characters are sent in
        intermediate frames with the last part of the message sent in an end
        frame. Intermediate frames terminate with the characters <ETB>,
        checksum, <CR> and <LF>
        """
        return ETB in self.frame and self.frame.index(ETB) >= 2

    @property
    def is_final(self):
        """A message containing 240 characters or less is sent in a single end
        frame. End frames terminate with the characters <ETX>, checksum, <CR>
        and <LF>
        """
        return ETX in self.frame and self.frame.index(ETX) >= 2

    @property
    def checksum_characters(self):
        """
        Checksum: The checksum permits the receiver to detect a defective
        frame. The checksum is encoded as two characters which are sent after
        the <ETB> or <ETX> character.
        """
        end = self.is_intermediate and ETB or ETX
        return self.frame[self.frame.index(end)+1:len(self.frame)-2]

    def is_valid(self):
        """Returns false if
        (1) Any character errors are detected (parity error, framing
            error, etc.),
        (2) The frame checksum does not match the checksum computed on the
            received frame,
        :return:
        """
        if not self.frame or len(self.frame) < 7:
            logger.error("No valid frame: len < 7")
            return False

        if self.frame[0] != STX:
            logger.error("No valid frame: STX not found")
            return False

        if self.frame[-2:] != CRLF:
            logger.error("No valid frame: CRLF not found")
            return False

        if not self.is_valid_fn():
            return False

        if all([self.is_intermediate, self.is_final]):
            # Both intermediate and final (ETB + ETX)
            logger.error("No valid frame: ETB + ETX")
            return False

        if not any([self.is_intermediate, self.is_final]):
            # Neither intermediate nor final
            logger.error("No valid frame: ETB or ETX is missing")
            return False

        # Leave the checksum check for later
        return self.is_valid_checksum()

    def is_valid_fn(self):
        """Returns whether the current frame number (fn) is valid or not. Frame
        number must be an int value between 0 and 7
        """
        try:
            fn = self.fn
        except:
            logger.error("No valid frame: FN")
            return False
        if fn < 0:
            logger.error("No valid frame: FN < 0")
            return False
        if fn > 7:
            logger.error("No valid frame: FN > 7")
            return False
        return True

    def calculate_checksum(self):
        """Checksum: The checksum permits the receiver to detect a defective
        frame. The checksum is encoded as two characters which are sent after
        the <ETB> or <ETX> character. The checksum is computed by adding the
        binary values of the characters, keeping the least significant eight
        bits of the result.

        The checksum is initialized to zero with the <STX> character. The first
        character used in computing the checksum is the frame number. Each
        character in the message text is added to the checksum (modulo 256).
        The computation for the checksum does not include <STX>, the checksum
        characters, or the trailing <CR> and <LF>.

        The checksum is an integer represented by eight bits, it can be
        considered as two groups of four bits. The groups of four bits are
        converted to the ASCII characters of the hexadecimal representation. The
        two ASCII characters are transmitted as the checksum, with the most
        significant character first.

        For example, a checksum of 122 can be represented as 01111010 in binary
        or 7A in hexadecimal. The checksum is transmitted as the ASCII character
        7 followed by the character A.
        """
        end = self.is_intermediate and ETB or ETX
        seed = map(ord, self.frame[1:self.frame.index(end) + 1])
        return hex(sum(seed) & 0xFF)[2:].upper().zfill(2).encode()

    def is_valid_checksum(self):
        """Returns whether the checksum for this frame is valid or not
        """
        try:
            expected = self.calculate_checksum()
            if expected == self.checksum_characters:
                return True
        except:
            pass
        logger.error("No valid frame: checksum")
        return False


class ASTMHandler(MessageHandler):
    """Generic ASTM receiver, compliant with ASTM-E1381-95 standard
    """

    messages = []
    in_transfer = False
    last_communication = None
    response = None

    def is_timeout(self):
        """Returns whether a timeout has been reached within a transfer phase
        """
        # During the transfer phase, the receiver sets a timer when first
        # entering the transfer phase or when replying to a frame. If a frame
        # or <EOT> is not received within 30 s, a timeout occurs. After a
        # timeout, the receiver discards the last incomplete message and regards
        # the line to be in the neutral state.
        is_timeout = False
        if self.in_transfer and self.last_communication:
            is_timeout = int(time.time()) - self.last_communication >= 30
        return is_timeout

    def get_full_message(self):
        """Returns the full message received
        """
        return CRLF.join(map(lambda m: m.text(), self.messages))

    def get_current_message(self):
        """Returns the last incomplete message or a new one
        """
        if not self.messages:
            self.messages = [Message()]

        if self.messages[-1].is_complete():
            last_message = self.messages[-1]
            start_fn = last_message.start_fn + len(last_message.frames)
            self.messages.append(Message(start_fn=start_fn))

        # Pop the last message
        return self.messages.pop()

    def is_busy(self):
        # TODO
        return self.response is not None

    def close(self):
        """Closes the current session and enters to neutral state
        """
        logger.info("* Entering Neutral state{}".format(CRLF))
        self.messages = []
        self.last_communication = None
        self.in_transfer = False

    def reset(self):
        self.close()

    def to_str(self, command):
        """Returns a human-readable representation of the command passed-in
        """
        if not command:
            return "EMPTY"

        if len(command) > 1:
            items = filter(None, list(command))
            items = "".join(map(self.to_str, items))
            return items

        if command in MAPPINGS:
            return MAPPINGS[command]

        return command

    def write(self, command):
        """Writes the command to the receiver
        """
        logger.debug("-> {}".format(self.to_str(command)))

        if self.is_busy():
            # A receiver that cannot immediately receive information, replies
            # with the <NAK> transmission control character. Upon receiving
            # <NAK>, the sender must wait at least 10 s before transmitting
            # another <ENQ>
            logger.info("Receiver is busy")
            self.response = NAK

        elif self.in_transfer:
            # Transfer Phase — During the transfer phase, the sender transmits
            # messages to the receiver. The transfer phase continues until all
            # messages are sent
            self.last_communication = int(time.time())
            if command.startswith(STX):
                # Reception of a frame
                self.response = self.write_frame(command)

            elif command.startswith(EOT):
                # End Of Transmission. Resume and enter to neutral state
                self.response = self.write_eot()

            else:
                # No valid message
                logger.error("No valid message. No <STX> or <EOT> received")
                self.response = NAK

        elif command == ENQ:
            # The system with information available initiates the establishment
            # phase. After the sender determines the data link is in a neutral
            # state, it transmits the <ENQ> transmission control character to
            # the intended receiver. Sender will ignore all responses other than
            # <ACK>, <NAK>, or <ENQ>.
            logger.info("{}* Establishment Phase completed".format(CRLF))
            logger.info("* Transfer Phase started ...")
            self.last_communication = int(time.time())
            self.in_transfer = True
            self.response = ACK

        else:
            # Establishment phase not yet initiated
            logger.error("Establishment phase not initiated")
            self.response = NAK

    def write_frame(self, frame_string):
        """
        The receiver replies to each frame. When it is ready to receive the
        next frame, it transmits one of three replies to acknowledge the last
        frame. This reply must be transmitted within the timeout period of 15s

        A reply of <NAK> signifies the last frame was not successfully received
        and the receiver is prepared to receive the frame again

        A reply of <ACK> signifies the last frame was received successfully and
        the receiver is prepared to receive another frame. The sender must
        increment the frame number and either send a new frame or terminate.

        A receiver checks every frame to guarantee it is valid. A reply of
        <NAK> is transmitted for invalid frames. Upon receiving the <NAK>, the
        sender retransmits the last frame with the same frame number. In this
        way, transmission errors are detected and automatically corrected.
        """
        # Are we in a transfer phase?
        if not self.in_transfer:
            # NAK response
            logger.error("Not in transfer phase")
            return NAK

        # Not successfully received or wrong. Reply <NAK>
        frame = Frame(frame_string)
        if not frame.is_valid():
            logger.error("Not a valid frame: {}".format(frame_string))
            return NAK

        logger.info("Frame {} received".format(frame.fn))

        # Get the message to work with (last if incomplete, or a new one)
        message = self.get_current_message()

        # Does this frame can be added to the message?
        if not message.can_add_frame(frame):
            logger.error("Cannot add frame to message")
            return NAK

        # Add the frame to the message
        message.add_frame(frame)

        # Add the message for the current transfer phase
        self.messages.append(message)

        # Response ACK
        return ACK

    def write_eot(self):
        """Handles an End Of Transmission message
        """
        message = self.messages and self.messages[-1] or None
        if not message:
            # Transmission without message
            logger.warn("No message transmitted")

        elif not message.is_complete():
            # Message is not complete
            logger.error("Message is not complete")

        else:
            # Message complete, notify
            logger.info("* Transfer Phase completed")
            self.notify()

        # Close transmission session
        self.close()

        return ACK

    def notify(self):
        """Prints the whole message in stdout
        """
        print("-" * 80)
        print(self.get_full_message())
        print("-" * 80)

    def read(self):
        if self.response:
            logger.debug("<- {}".format(self.to_str(self.response)))
        resp = self.response
        self.response = None
        return resp


class ASTMToSenaiteHandler(ASTMHandler):
    """ASTM receiver that is capable to directly send the results to SENAITE
    """

    def __init__(self, url, user, password, **kwargs):
        super(ASTMToSenaiteHandler, self).__init__(**kwargs)
        self._url = url
        self._user = user
        self._password = password
        self._retries = kwargs and kwargs.get("retries") or 5
        self._delay = kwargs and kwargs.get("delay") or 10
        self._dry_run = kwargs and kwargs.get("dry-run") or False

    def notify(self):
        super(ASTMToSenaiteHandler, self).notify()

        if self._dry_run:
            # Dry Run. Do not notify SENAITE LIMS
            return

        if self.messages:
            # Notify SENAITE LIMS
            thread = threading.Thread(target=self.notify_senaite,
                                      args=(self.messages,))
            thread.start()

    def notify_senaite(self, messages):
        # Number of retries and delay in seconds between retries
        retries = self._retries >= 0 and self._retries + 1 or 4
        delay = self._delay > 0 and self._delay or 5

        # Build the POST payload
        payload = {
            "consumer": "senaite.serial.astm.import",
            "messages": messages,
        }

        # Try to push messages to SENAITE
        success = False
        while retries > 0:

            # Open a session with SENAITE and authenticate
            session = lims.Session(self._url, self._user, self._password)
            authenticated = session.auth()
            if authenticated:

                # Send the message
                response = session.post("push", payload)
                success = response.get("success")
                if success:
                    break

            # Sleep before we retry
            time.sleep(delay)
            retries -= 1

            if retries > 0:
                logger.warn("Could not push. Retrying {}/{}".format(
                    self._retries - retries + 1, self._retries
                ))

        if not success:
            logger.error("Could not push the message")
