import configparser, os, logging, datetime

conf = configparser.ConfigParser()
conf.read(os.path.join('data', 'config.ini'))

'''def validate(type):
  match type.lower():
    case "email":
      try:
        return data.index("@") < data.rindex(".")
      except Exception:
        return False
    case "gateway":
      if conf['Scheduler']['gateway'] == "":

    case "path" or "paths":
      pass
    case _:
      return False'''

def genLogger(path, level=logging.DEBUG, format="[%(asctime)s][%(levelname)s]: %(message)s"):
    today = datetime.datetime.today()
    if today.hour < 10:
        hour = "0{}".format(today.hour)
    else:
        hour = today.hour
    if today.minute < 10:
        minute = "0{}".format(today.minute)
    else:
        minute = today.minute

    logFile = os.path.join(path, "log-{}-{}-{}-{}{}".format(today.year,today.month,today.day,hour,minute))
    logging.basicConfig(filename=logFile,format=format,level=logging.DEBUG,force=True)
    return "logging.basicConfig(filename={},format={},level={},force=True)\nlogger = logging.getLogger(__name__)".format(logFile, format, level)

def genConfigFile():
    """Generates a config file"""

    with open(os.path.join('data', 'config.ini'), 'w') as f:
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
        f.write("public_key_path = {}\n\n".format(os.path.join('data','public.pem')))

        f.write("; The path to take to the private key file\n")
        f.write("private_key_path = {}\n\n".format(os.path.join('data','private.pem')))

        f.write("; Path to file containing the email\n")
        f.write("email_path = {}\n\n".format(os.path.join('data','email.bin')))
        
        f.write("; Path to file containing the password\n")
        f.write("password_path = {}".format(os.path.join('data','pass.bin')))