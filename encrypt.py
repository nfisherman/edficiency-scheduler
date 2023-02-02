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

import sys, os.path, configparser
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

A_VERSION = "0.1"

args = sys.argv[1:]

key = RSA.generate(2048)

def genConfigFile():
    """Generates a config file"""

    with open('data/config.ini', 'w') as f:
        f.write("[Scheduler]\n")

        f.write("; The login page to target\n")
        f.write("gateway = \n\n")

        f.write("; The last name of the teacher you want to attend on each day of the week\n")
        f.write("; Enter an empty string for none\n")
        f.write("monday_name = \n")
        f.write("tuesday_name = \n")
        f.write("wednesday_name = \n")
        f.write("thursday_name = \n")
        f.write("friday_name = \n\n")

        f.write("[Auth]\n")

        f.write("; Decides whether or not to encrypt\n")
        f.write("; STRONGLY RECOMMNEDED TO KEEP THIS ENABLED\n")
        f.write("encrypted = True\n\n")

        f.write("; The sign in method to use ((0) Edficiency, (1) Google, (2) Microsoft)\n")
        f.write("; Currently, sign in with Microsoft and accounts with 2FA are not supported\n")
        f.write("sign_in_method = 0\n\n")

        f.write("; The path to take to the public key file\n")
        f.write("public_key_path = data/public.pem\n\n")

        f.write("; The path to take to the private key file\n")
        f.write("private_key_path = data/private.pem\n\n")

        f.write("; Path to file containing the email\n")
        f.write("email_path = data/email.bin\n\n")
        
        f.write("; Path to file containing the password\n")
        f.write("password_path = data/pass.bin")

conf = configparser.ConfigParser()
if not os.path.isfile('data/config.ini'):
    genConfigFile()
conf.read('data/config.ini')

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