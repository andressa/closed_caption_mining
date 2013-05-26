#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title:       ClosedCaption.py
Author:      Andressa Sivolella <asivolella@poli.ufrj.br>
Date:        2013-05-25
"""

import os
import sys
from datetime import datetime
import serial

from django.core.management import setup_environ
sys.path.append(os.path.normpath(os.path.join( os.path.dirname(os.path.realpath(__file__)), '../../')))
import siteconfig.settings
setup_environ(siteconfig.settings)

from cc_mining.models import ClosedCaption

USBDEVICE = '/dev/tty.usbmodemfa131'
RESPONSE = {
            0: 'ARDUINO CONNECTED! LETS GET CLOSED CAPTIONS',
            1: 'ARDUINO IS NOT CONNECTED!',
           }
VERBOSE = True

class ClosedCaptionHandler(object):
    """
    Package to handle closed caption acquisition from Video Experimenter
    and Arduino Uno
    """
    def __init__(self, usb_device=USBDEVICE, verbose=VERBOSE):
        """
        Initializing object: setting usb path
        """
        self.usb_device = usb_device
        self.verbose = verbose
        self.closed_caption = {}

        if not self.open_arduino_conn():
            if self.verbose:
                print RESPONSE[1]
        else:
            if self.verbose:
                print RESPONSE[0]

    def open_arduino_conn(self):
        """
        Start reading usb device output, sent by Arduino
        """
        try:
            self.arduino = serial.Serial(self.usb_device, 57600)
        except serial.serialutil.SerialException:
            return False
        return True

    def get(self):
        try:
            while True:
                try:
                    cc_received = self.arduino.readline()
                    self.closed_caption[datetime.now()] = cc_received
                    cc_line, created = ClosedCaption.objects.get_or_create(
                        closed_caption = cc_received
                    )
                    cc_line.save()
                except serial.serialutil.SerialException:
                    pass
        except KeyboardInterrupt:
            self.stop_acquisition()

    def clean_text(self, text):
        """
        Recover special characters, found in latin languages
        """
        pass

    def stop_acquisition(self):
        self.close_arduino_conn()
        if self.verbose:
            for timestamp, cc_line in self.closed_caption.iteritems():
                print timestamp, cc_line

    def close_arduino_conn(self):
        self.arduino.close()

