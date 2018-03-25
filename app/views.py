from app import app
from flask import jsonify, request, send_from_directory
import json
import os


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
  if (path == ""):
    return send_from_directory('../app/build', 'index.html')
  else:
    if (os.path.exists("app/build/" + path)):
      return send_from_directory('../app/build', path)
    else:
      return send_from_directory('../app/build', 'index.html')


@app.route('/profiles')
def get_profiles():
  profiles = json.load(open("profiles.json"))
  return jsonify(profiles)


@app.route('/config', methods=['GET', 'POST'])
def get_config():
  if request.method == 'POST':
    config = request.json
    with open('config.json', 'w') as outfile:
      json.dump(config, outfile, sort_keys=True, indent=4)
    return "Success"
  else:
    config = json.load(open("config.json"))
    return jsonify(config)
