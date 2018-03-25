#!/usr/bin/python3

import os
import json
import datetime
import pickle
import pprint
from geolite2 import geolite2
from copy import deepcopy

database = {}
config = json.load(open("config.json"))


class PythonObjectEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
      return json.JSONEncoder.default(self, obj)
    return {'_python_object': pickle.dumps(obj)}


pp = pprint.PrettyPrinter(indent=4)


def set_default(obj):
  if isinstance(obj, set):
    return list(obj)
  raise TypeError


def getOnlyIPs(data):
  IPs = []
  for key, value in data.items():
    IPs.append(key)
  return IPs


def addtoWordList(data):
  userpass = (data["username"], data["password"])
  database[data["src_ip"]]["wordlist"].add(userpass)


def loginSuccess(data):
  database[data["src_ip"]]["successfulLogins"] += 1
  addtoWordList(data)


def loginFailed(data):
  database[data["src_ip"]]["failedLogins"] += 1
  addtoWordList(data)


def commandInput(data):
  time = datetime.datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
  timecommand = (time, data["input"])
  database[data["src_ip"]]["commands"].append(timecommand)


def fileDownload(data):
  download = (data["shasum"], data["url"], data["url"].split("/")[-1], "/".join(data["url"].split("/")[:-1]))
  database[data["src_ip"]]["downloads"].add(download)


def locationData(data):
  reader = geolite2.reader()
  location = reader.get(data["src_ip"])
  if location is not None:
    database[data["src_ip"]]["location"] = location


def clientVersion(data):
  database[data["src_ip"]]["client"].add(data["version"])


def correlateFilename(data, filename):
  correlatedData = {}
  for key, value in data.items():
    for file in value["downloads"]:
      if file[2] == filename:
        correlatedData[key] = value
  return correlatedData


def correlateSHA(data, SHA):
  correlatedData = {}
  for key, value in data.items():
    for file in value["downloads"]:
      if file[0] == SHA:
        correlatedData[key] = value
  return correlatedData


def correlateHost(data, host):
  correlatedData = {}
  for key, value in data.items():
    for file in value["downloads"]:
      if file[3] == host:
        correlatedData[key] = value
  return correlatedData


def correlateURL(data, url):
  correlatedData = {}
  for key, value in data.items():
    for file in value["downloads"]:
      if file[1] == url:
        correlatedData[key] = value
  return correlatedData


def handelEvent(data):
  if data["src_ip"] not in database.keys():
    database[data["src_ip"]] = {"successfulLogins": 0, "failedLogins": 0, "wordlist": set(), "commands": [],
                                "downloads": set(), "client": set(), "location": {}}
    locationData(data)

  if data["eventid"] == "cowrie.login.success":
    loginSuccess(data)
  elif data["eventid"] == "cowrie.login.failed":
    loginFailed(data)
  elif data["eventid"] == "cowrie.command.input":
    commandInput(data)
  elif data["eventid"] == "cowrie.session.file_download":
    fileDownload(data)
  elif data["eventid"] == "cowrie.client.version":
    clientVersion(data)


def readFiles():
  for file in os.listdir(config["honeypotpath"]):
    with open(config["honeypotpath"] + "/" + file) as jsonFile:
      for line in jsonFile:
        data = json.loads(line)
        handelEvent(data)


def generateSuricataRules(profiles):
  file = open(config["rulepath"] + "drop_profiles.rule", "w")
  for key, value in profiles.items():
    for ip in value["new"]:
      if ip not in config["whitelist"]:
        rule = 'drop ip {ip} any -> any any (msg:"{ip} dropped from profile {profile}"; sid:1;)\n'.format(ip=ip,
                                                                                                          profile=key)
        file.write(rule)
  for ip in config["blacklist"]:
    if ip not in config["whitelist"]:
      rule = 'drop ip {ip} any -> any any (msg:"{ip} dropped from blacklist"; sid:1;)\n'.format(ip=ip)
      file.write(rule)


readFiles()

i = 0
tempDict = {}
for key, value in database.items():
  if len(database[key]["downloads"]) > 0:
    i += 1
    tempDict[key] = value

filesDownloaded = set()

for key, value in tempDict.items():
  for file in value["downloads"]:
    filesDownloaded.add(file[2])

profiles = {}


def make_profile(corr_files, profile, database3):
  for key, value in corr_files.items():
    for download in value["downloads"]:
      similar_shas = getOnlyIPs(correlateSHA(database3, download[0]))
      for ip in similar_shas:
        database2.pop(ip, None)
        profile.add(ip)
      similar_hosts = getOnlyIPs(correlateHost(database3, download[3]))
      for ip in similar_hosts:
        database2.pop(ip, None)
        profile.add(ip)
  return profile


for file in filesDownloaded:
  corr_files = correlateFilename(tempDict, file)
  database2 = deepcopy(database)
  profile = set()
  for key, value in corr_files.items():
    database2.pop(key, None)
    profile.add(key)
  profiles[file] = {"initial": list(deepcopy(profile))}
  completed_profile = make_profile(corr_files, profile, database2)
  profiles[file]["new"] = list(completed_profile)

pp.pprint(profiles)

if config["ruletype"] == "suricata":
  generateSuricataRules(profiles)

file = open("profiles.json", "w")
file.write(json.dumps(profiles, indent=4, sort_keys=True))
