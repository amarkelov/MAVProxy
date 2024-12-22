#!/usr/bin/env python
'''
control MAVLink2 encryption
'''

from pymavlink import mavutil
import time
import sys

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util

if mp_util.has_wxpython:
    from MAVProxy.modules.lib.mp_menu import *


class EncryptionModule(mp_module.MPModule):

    def __init__(self, mpstate):
        super(EncryptionModule, self).__init__(mpstate, "encryption", "encryption control", public=True)
        self.add_command('encryption', self.cmd_encryption, "encryption control",
                         ["<enable|disable|rekey>"])
        self.allow = None

    def cmd_encryption(self, args):
        '''handle link commands'''
        usage = "encryption: <enable|disable|rekey>"
        if len(args) == 0:
            print(usage)
        elif args[0] == 'enable':
            self.cmd_encryption_enable()
        elif args[0] == 'rekey':
            self.cmd_encryption_rekey()
        elif args[0] == 'disable':
            self.cmd_encryption_disable()
        else:
            print(usage)

    def cmd_encryption_enable(self):
        '''setup encryption'''
        if not self.master.mavlink20():
            print("You must be using MAVLink2 for encryption")
            return
        public_key = bytearray()
        public_key_signature = bytearray()
        cipher = 0
        iv = bytearray()

        for b in bytes(range(1, 66)):
            public_key.append(b)
        for b in bytes(range(1, 65)):
            public_key_signature.append(b)

        for b in bytes(range(1, 3)):
            iv.append(b)

        self.master.mav.setup_encryption_send(self.target_system,
                                              self.target_component,
                                              public_key,
                                              public_key_signature,
                                              cipher,
                                              iv)
        print("Sent request to setup encryption")
#        self.cmd_encryption_rkey()

    def cmd_encryption_rekey(self):
        '''initiate change of encryption key'''
        if not self.master.mavlink20():
            print("You must be using MAVLink2 for encryption")
            return
        # self.master.setup_encryption(key, sign_outgoing=True, allow_unsigned_callback=self.allow_unsigned)
        print("Changed session encryption key")

    def cmd_encryption_disable(self):
        '''disable encryption locally'''
        self.master.disable_encryption()
        print("Disabled encryption")

    def cmd_encryption_remove(self):
        '''remove encryption from server'''
        if not self.master.mavlink20():
            print("You must be using MAVLink2 for encryption")
            return
        self.master.mav.setup_encryption_send(self.target_system, self.target_component, [0]*32, 0)
        self.master.disable_encryption()
        print("Removed encryption")

def init(mpstate):
    '''initialise module'''
    return EncryptionModule(mpstate)
