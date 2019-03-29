import requests
from bs4 import BeautifulSoup
import time
import json
import pathlib
import getpass
import logging

def loadUser():
    p = pathlib.Path("user.json")
    if p.is_file():
        try:
            with p.open() as f:
                user_info = json.load(f)
                return user_info
        except OSError:
            logger.error("Error trying to open the user info file (user.json)!")
            return 255
    else:
        return -1

def deleteConfig():
    p = pathlib.Path("user.json")
    if p.is_file():
        p.unlink()



def checkScores():
    url = "https://account.collegeboard.org/login/authenticateUser"
    headers = {
        "authority": "account.collegeboard.org",
        "scheme": "https",
        "origin": "https://account.collegeboard.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Referer": "https://account.collegeboard.org/login/authenticateUser"
        }
    data = {
        "DURL": "https://nsat.collegeboard.org/satweb/satHomeAction.action",
        "appId": "319",
        "formState": "1",
        "username": input("Your username: "),
        "password": input("Your password: "),
        "sign-in": ""
        }
    s = requests.Session()
    r = s.post(url, data=data, headers=headers)

    if r.status_code == 200:
        #if
        if "don\'t recognize" in r.text:
            deleteConfig()
            logger.error("Your login credentials are invalid. Try again?")
            exit(255)
        #'''elif "We don't recognize that username and password." in r.text:
        #    deleteConfig()
        #    print("[", int(time.time()), "] ", "Your login credentials are invalid. (Wrong password?) Try again?", sep="")
        #    exit(255)'''
        else:
            logger.info("Login successful!")
        #print(r.text)
    else:
        logger.error("Login failed! Exiting...")
        # a non-200 response code means errors other than incorrect username/pwd
        logger.debug(r.text)
        #ifttt post here
        exit(255)
    soup = BeautifulSoup(r.text, features="html.parser")
    scores = soup.find_all("div", {"class": "col-sm-7 col-xs-12 cb-base-font-size"})
    for i in range(len(scores)):
        tmp = scores[i].get_text()
        '''tmp = tmp.replace("\n\n\n\n\n \n", "")
        tmp = tmp.replace("\n\n\n", "")
        tmp = tmp.replace(" \n", "")
        tmp = tmp.replace("\n\n", "")
        tmp = tmp.replace(" SAT", "SAT")
        print(i+1, ": ", tmp, sep="")'''
        tmp = tmp.replace("\n\n\n\n\n \n", "")
        tmp = tmp.replace("\n\n\n", "")
        tmp = tmp.replace(" \n", "")
        tmp = tmp.replace("\n\n", "")
        tmp = tmp.replace(" SAT", "SAT")
        tmp = tmp.replace("Total Score", "")
        logger.info(str(i+1) + ": " + tmp + "\n")

    #ifttt here
'''    for i in range(len(scores)):
        if len(scores[i]) >= 4:
            print(scores[i])'''

def checkScoresDiff(usr, pwd):
    url = "https://account.collegeboard.org/login/authenticateUser"
    headers = {
        "authority": "account.collegeboard.org",
        "scheme": "https",
        "origin": "https://account.collegeboard.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Referer": "https://account.collegeboard.org/login/authenticateUser"
        }
    data = {
        "DURL": "https://nsat.collegeboard.org/satweb/satHomeAction.action",
        "appId": "319",
        "formState": "1",
        "username": usr,
        "password": pwd,
        "sign-in": ""
        }
    s = requests.Session()
    r = s.post(url, data=data, headers=headers)
    #print(r.text)
    #print("Sorry, we don\'t recognize" in r.text == 1)
    if r.status_code == 200:
        #if
        if "don\'t recognize" in r.text:
            deleteConfig()
            logger.error("Your login credentials are invalid. Try again?")
            exit(255)
        else:
            logger.info("Login successful!")
        #print("[", int(time.time()), "] ", "Login successful", sep="")
        #print(r.text)
    else:
        logger.error("Request failed with a status code of " + str(r.status_code) + ". Exiting...")
        # a non-200 response code means errors other than incorrect username/pwd
        logger.debug(r.text)
        #ifttt post here
        exit(255)
    soup = BeautifulSoup(r.text, features="html.parser")
    scores = soup.find_all("div", {"class": "col-sm-7 col-xs-12 cb-base-font-size"})

    tmp = scores[0].get_text()

    tmp = tmp.replace("\n\n\n\n\n \n", "")
    tmp = tmp.replace("\n\n\n", "")
    tmp = tmp.replace(" \n", "")
    tmp = tmp.replace("\n\n", "")
    tmp = tmp.replace(" SAT", "SAT")
    tmp = tmp.replace("Total Score", "")
    res = tmp
    return res

logger = logging.getLogger('sat_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('SATScoreChecker.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

if pathlib.Path("user.json").is_file():
    logger.info("Loading CollegeBoard account info from file \"user.json\"...")
    user_info = loadUser()
    u = user_info.get("username")
    p = user_info.get("password")
    logger.info("Logging in as: " + u)
else:
    u = input("Your username: ")
    p = getpass.getpass("Your password (input won't be echoed): ")
    acct_dict = {
        "username": u,
        "password": p
    }
    f = open("user.json", "w+")
    json.dump(acct_dict, f)
    f.close()





prevResults = checkScoresDiff(u, p)
logger.info(prevResults)
time.sleep(20)
while True:
    curResults = checkScoresDiff(u, p)
    #print(curResults)
    if curResults != prevResults:
        logger.warning("New scores posted!")
        logger.info(curResults)
        if os.name == "nt":
            os.system("pause")
        else:
            exit(0)
    time.sleep(20)
