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

import sys, configparser, datetime, os, logging, redist
# TO-DO: Add GUI
# from guizero import *
from inputimeout import inputimeout
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

A_VERSION = "0.2"

args = sys.argv[1:]
conf = configparser.ConfigParser()
conf.read(os.path.join('data', 'config.ini'))
public_key = conf['Auth']['public_key_path']

exec(redist.genLogger(conf['Logging']['log_path']))

while len(os.listdir(conf['Logging']['log_path'])) > int(conf['Logging']['max_logs']) and not int(conf['Logging']['max_logs']) == 0:
  min = conf['Logging']['log_path'] + '/' + os.listdir(conf['Logging']['log_path'])[0]

  for x in os.listdir(conf['Logging']['log_path'])[1:]:
    if os.path.getctime(conf['Logging']['log_path'] + '/' + x) < min:
      min = conf['Logging']['log_path'] + '/' + x
  
  os.remove(min)

def main():
  driver = webdriver.Chrome()

  validate("gateway")
  validate("email")
  # Generated by Selenium IDE
  if conf['Scheduler']['gateway'] == "":
    logMsg("Edficiency gateway not defined. Check config file.")
    sys.exit("Edficiency gateway not defined. Check config file.")
  elif not conf['Scheduler']['gateway'][conf['Scheduler']['gateway'].index("."):] == ".edf.school":
    logMsg("Edficiency gateway validation failed. Continue anyways? [y/N]", "WARN")
    try:
      user = inputimeout(prompt="Edficiency gateway validation failed. Continue anyways? [y/N] ", timeout=conf['Logging']['timeout'])
      user.strip()
      logMsg("\"" + user + "\"", "USER")
    except Exception:
      user = "N"
      logMsg("User input timeout, defaulting to 'N'", "NOTICE")
    finally:
      if user.upper() == "N" or user == "":
        logMsg("Edficiency gateway validation failed. Check config file.")
        sys.exit("Edficiency gateway validation failed. Check config file.")
  else:
    logMsg("Edficiency gateway validation success.", "NOTICE")

  driver.get(conf['Scheduler']['gateway'])
  driver.set_window_size(1385, 875)

  match int(conf['Auth']['sign_in_method']):
    case 1:
      try:
        # Click "Sign in with Google" button
        driver.find_element(By.CSS_SELECTOR, '.login-btn:nth-child(1) > .my-auto').click()

        try:
          # Open the email file
          with open(conf['Auth']['email_path'], 'rb') as f:
            contents = f.read()
            
            # If encrypted, unencrypt
            if bool(conf['Auth']['encrypted']):
              cipher = PKCS1_OAEP.new(RSA.importKey(open(conf['Auth']['private_key_path']).read()))
              contents = cipher.decrypt(contents)

            if not validate(contents.decode('UTF-8'), "email"):
              logMsg("Email validation failed. Continue anyway? [y/N] ", "WARN")
              try:
                user = inputimeout(prompt="Email validation failed. Continue anyway? [y/N] ", timeout=conf['Logging']['timeout'])
                user.strip()
                logMsg("\"" + user + "\"", "USER")
              except Exception:
                user = "N"
                logMsg("User input timeout, defaulting to 'N'", "NOTICE")
              finally:
                if(user.upper() == "N" or user == ""):
                  logMsg("Email validation failed. Check config file.")
                  sys.exit("Email validation failed. Check config file.")

            driver.find_element(By.ID, 'identifierId').send_keys(contents.decode('UTF-8'))
              
            driver.find_element(By.ID, 'identifierId').send_keys(Keys.ENTER) 
        except Exception:
          logMsg("Email not defined. Check config file.")
          sys.exit("Email not defined. Check config file.")
        
        try:
          # Open the password file
          with open(conf['Auth']['password_path'], 'rb') as f:
            contents = f.read()

            # If encrypted, unencrypt
            if bool(conf['Auth']['encrypted']):
              cipher = PKCS1_OAEP.new(RSA.importKey(open(conf['Auth']['private_key_path']).read()))
              contents = cipher.decrypt(contents)

            driver.find_element(By.NAME, 'password').send_keys(contents.decode('UTF-8'))

            driver.find_element(By.ID, 'identifierId').send_keys(Keys.ENTER)
        except Exception:
          logMsg("Password not defined. Check config file.")
          sys.exit("Password not defined. Check config file.")
      except Exception:
        logMsg("Login failed.")
        sys.exit("Login failed.")
    case 2:
      logMsg("Microsoft login is currently not supported. Change login method in config file.")
      sys.exit("Microsoft login is currently not supported. Change login method in config file.")

    case 0:
      try:
        driver.find_element(By.ID, "email").click()

        try:
          # Open the email file
          with open(conf['Auth']['email_path'], 'rb') as f:
            contents = f.read()

            # If encrypted, unencrypt
            if bool(conf['Auth']['encrypted']):
              cipher = PKCS1_OAEP.new(RSA.importKey(open(conf['Auth']['private_key_path']).read()))
              contents = cipher.decrypt(contents)

              if contents.decode('UTF-8') == "":
                logMsg("Email not defined. Check config file.")
                sys.exit("Email not defined. Check config file.")
              elif not validate(contents.decode('UTF-8')):
                logMsg("Email validation failed. Continue anyway? [y/N]", "WARN")
                try:
                  user = inputimeout(prompt="Email validation failed. Continue anyway? [y/N] ", timeout=conf['Logging']['timeout'])
                  user.strip()
                  logMsg("\"" + user + "\"", "USER")
                except Exception:
                  user = "N"
                  logMsg("User input timeout, defaulting to 'N'", "NOTICE")
                finally:
                  if(user.upper() == "N" or user == ""):
                    logMsg("Email validation failed. Check config file.")
                    sys.exit("Email validation failed. Check config file.")

              driver.find_element(By.ID, "email").send_keys(contents.decode('UTF-8'))
        except Exception:
          logMsg("Email not defined. Check config file.")
          sys.exit("Email not defined. Check config file.")

        driver.find_element(By.ID, "password").click()

        # Open the password file
        with open(conf['Auth']['password_path'], 'rb') as f:
          contents = f.read()

          # If encrypted, unencrypt
          if bool(conf['Auth']['encrypted']):
            cipher = PKCS1_OAEP.new(RSA.importKey(open(conf['Auth']['private_key_path']).read()))
            contents = cipher.decrypt(contents)

          if(contents.decode('UTF-8') == ""):
            logMsg("Password not defined. Check config file.")
            sys.exit("Password not defined. Check config file.")

          driver.find_element(By.ID, "password").send_keys(contents.decode('UTF-8'))

        driver.find_element(By.ID, "btnLogin").click()

      except Exception:
        logMsg("Login failed.")
        sys.exit("Login failed.")
    case _:
      logMsg("Login method invalid or not defined. Check config file.")
      sys.exit("Login method invalid or not defined. Check config file.")


  
  # Go to the "Request Sessions" page
  driver.find_element(By.CSS_SELECTOR, 'li:nth-child(3) > a').click()

  # Adds the teachers' names to a list
  teachers = list(range(5))
  teachers[0] = conf['Scheduler']['monday_name'].split("|")
  teachers[1] = conf['Scheduler']['tuesday_name'].split("|")
  teachers[2] = conf['Scheduler']['wednesday_name'].split("|")
  teachers[3] = conf['Scheduler']['thursday_name'].split("|")
  teachers[4] = conf['Scheduler']['friday_name'].split("|")
  
  
  for i in range(1,5):
    for j in teachers[i]:
      if not j == "":
        
        driver.find_element(By.CSS_SELECTOR, '.col > .form-control').click()
        
        log = 1

        while(not log == 0):
          try:
            driver.find_element(By.CSS_SELECTOR, '.col > .form-control').send_keys(j)
            
            date = datetime.date.today() + datetime.timedelta(days=i)
            date_formatted = "//*[text()='" + date.strftime("%A, %B %-mnd") + "']"
            driver.find_element(By.XPATH, date_formatted).click()

            # logMsg()
          except Exception:
            pass
        
        driver.find_element(By.ID, 'lowButton').click()

def logMsg(message, type="EXIT"):
  if not int(conf['Logging']['max_logs']) == 0:
    with open(logFile, "a") as f:
      f.write("[" + currDateAndTime() + "][" + type.upper() + "] " + message)
      return True
  
  return False

def validate(type):
  match type.lower():
    case "email":
      try:
        return data.index("@") < data.rindex(".")
      except Exception:
        return False
    case "gateway":
      
    case _:
      return False


def currDateAndTime():
  return today.year + "-" + today.month + "-" + today.day + " " + today.hour + ":" + today.minute

# TO-DO: Add GUI
# def draw():
#   app = App(bg = "#e8e8e8", title='Edficiency Scheduler')
#   if conf['Scheduler']['gateway'] == "":
#     prompt = Text(app, text="Enter in your Edficiency login portal:")
#     inputBox = TextBox(app)
#     confirmButton = PushButton(app, text="Confirm", command=verify(app, prompt, inputBox))
    
  
#   if conf['Auth']['email'] == "":
#     pass

# TO-DO: Add GUI
# def verify(app, prompt, input):
#   match prompt.value:
#     case "Enter in your Edficiency login portal:":
#       if("@" in prompt.value):

#         draw()
#       else:
#         error = Text(app, text="Invalid email")
#         error.text_color = "red"


if '-h' in args:
  print('Placeholder')
# TO-DO: Add GUI
# elif '-nogui' in args:
#   main()
else:
  #draw()
  main()