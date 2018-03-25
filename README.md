# Custom Network Security Appliance

This custom network security appliance was created as part of a Senior Theisis Project at Eastern Michigan University. This repo contains the necessary files to turn Suricata into my *self learning* custom network security appliance. In short, it collects data from the [Cowrie](https://github.com/micheloosterhof/cowrie) honeypot, processes it in my custom framework to create profiles for attackers, then formats those profiles into Suricata rules and outputs them for Suricata to ingest.

## Requirements

 - [Suricata](https://github.com/OISF/suricata)
 - [Cowrie](https://github.com/micheloosterhof/cowrie)
 - [Python3](https://www.python.org/downloads/)
 - [Flask](https://github.com/pallets/flask)
 - [Flask-Cors](https://github.com/corydolphin/flask-cors)
 - [maxminddb-geolite2](https://dev.maxmind.com/geoip/geoip2/geolite2/)

## Setup

 1. Install Suricata on a linux operating system and set it up in inline mode
 2. Install the Cowrie honeypot and configure it to output its rules to JSON format
 3. Clone this repo
 4. Run `sudo pip install -r requirements.txt`
 5. Run `python3 webapp.py`
 6. Go to http://localhost:5000/config in your browser
 7. Configure the honeypot log path with the directory where the json log files live
 8.  Configure the rule file path to where you would like the rule file to output to
 9. Click Save
 10. Setup `framework.py` to run in a cron jon every day (this is when new rules will be generated)
 11. Configure Suricata to read rules from the outputted rule file

