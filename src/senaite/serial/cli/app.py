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

import argparse
import logging
import sys

import serial
from serial.serialutil import to_bytes

import lims
from . import logger
from .lis1a import LIS1AHandler
from .lis1a import LIS1AToSenaiteHandler


def start_server(port, baud_rate, receiver):
    """Start serial server. Keeps listening to the given port at the baud rate
    specified and writes the commands coming in to the receiver
    :param port: the serial port address to listen at
    :param baud_rate: the data transmission rate
    :param receiver: the receiver in charge of handling the incoming messages
    """
    with serial.Serial(port, baud_rate, timeout=2) as ser:
        print("Listening on port {}, press Ctrl+c to exit.".format(port))
        while True:
            if receiver.is_timeout():
                logger.warn("Timeout")
                receiver.reset()

            # Read from the sender
            line = ser.readline()
            if not line:
                continue

            # Notify the receiver with the new command
            receiver.write(line)

            # Does the receiver has to send something back?
            response = receiver.read()
            if response:
                socket = serial.Serial(port, baud_rate, timeout=10)
                socket.write(to_bytes(response))


def get_receiver(args):
    """Returns the receiver in charge to handle the incoming messages based on
    the arguments passed-in
    """
    params = {
        "dry-run": args.dry_run,
        "retries": args.retries,
        "delay": args.delay,
    }
    if args.url:
        # SENAITE URL provided
        try:
            info = lims.get_senaite_connection_info(args.url)
            params.update(info)
        except Exception as e:
            logger.error(e.message)
            sys.exit(-1)

        # LIS1A-to-SENAITE handler
        receiver = LIS1AToSenaiteHandler(**params)

    else:
        # Basic LIS1-A handler
        receiver = LIS1AHandler(**params)

    return receiver


def main():
    """Application entry-point
    """
    parser = argparse.ArgumentParser(
        description="SENAITE Serial client interface",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Positional arguments
    parser.add_argument("port", help="COM Port to connect. Serial client will "
                                     "listen to this port for incoming data "
                                     "and use this same port to send data back")

    # Optional arguments
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Verbose logging")

    parser.add_argument("-b", "--baudrate",
                        type=int, default=9600,
                        help="Baudrate")

    parser.add_argument("-u", "--url", type=str,
                        help="SENAITE full URL address, with username and "
                             "password: "
                             "'http(s)://<user>:<password>@<senaite_url>'. ")

    parser.add_argument("-r", "--retries", type=int,
                        default=3,
                        help="Number of attempts of reconnection when SENAITE "
                             "instance is not reachable. Only has effect when "
                             "argument --url is set")

    parser.add_argument("-d", "--delay", type=int,
                        default=5,
                        help="Time delay in seconds between retries when "
                             "SENAITE instance is not reachable. Only has "
                             "effect when argument --url is set")

    parser.add_argument("-t", "--dry-run",
                        action="store_true",
                        help="Dry run. Data won't be sent to SENAITE instance. "
                             "This argument only has effect when argument "
                             "--url is set")

    args = parser.parse_args()

    # Set logging
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # Instantiate the receiver
    receiver = get_receiver(args)

    # Start the server
    start_server(args.port, args.baudrate, receiver)


if __name__ == "__main__":
    main()
