#!/usr/bin/env python3

# Copyright (c) 2022-2023 nfisherman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sys, os, configparser, redist
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

A_VERSION = "0.1"

args = sys.argv[1:]

key = RSA.generate(2048)

conf = configparser.ConfigParser()
if not os.path.isfile(os.path.join('data','config.ini')):
    redist.genConfigFile()
conf.read(os.path.join('data','config.ini'))

def genPrivateKey():
    """Generates a private key"""

    prv_key_string = key.exportKey()
    with open(conf['Auth']['private_key_path'], "w") as prv:
        print("{}".format(prv_key_string.decode()), file=prv)

def genPublicKey():
    """Generates a public key"""

    pub_key_string = key.publickey().exportKey()
    with open(conf['Auth']['public_key_path'], "w") as pub:
        print("{}".format(pub_key_string.decode()), file=pub)

def encrypt():
    """Encrypts the email and password using the previously generated public key"""

    cipher = PKCS1_OAEP.new(RSA.importKey(open(conf['Auth']['public_key_path']).read()))
    email = cipher.encrypt(input("What is your email? ").encode('UTF-8'))
    password = cipher.encrypt(input("What is your password? ").encode('UTF-8'))

    with open(conf['Auth']['email_path'], 'wb') as f:
        f.write(email)

    with open(conf['Auth']['password_path'], 'wb') as f:
        f.write(password)
    
if "-h" in args:
    print('Placeholder')
elif bool(conf['Auth']['encrypted']):
    if not os.path.isfile(conf['Auth']['private_key_path']) or "-prv" in args:
        genPrivateKey()

    if not os.path.isfile(conf['Auth']['public_key_path']) or "-pub" in args:
        genPublicKey()

    encrypt()
else:
    with open(conf['Auth']['email_path'], 'wb') as f:
        f.write(input("What is your email? ").encode('UTF-8'))
    
    with open(conf['Auth']['password_path'], 'wb') as f:
        f.write(input("What is your password? ").encode('UTF-8'))