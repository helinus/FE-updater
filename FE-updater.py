#!/usr/bin/env python

# Put this Python 2.7.5 file in the same folder as your minecraft jar.

# Only if there's a newer build will it download the server zip file.
# When run it fetches the latest build timestamp and compares it to
# that of the build it downloaded last and after that it removes the
# old core, modules and libs and extracts the new ones.

import json
import shutil
import zipfile
import urllib
import re
import os

prevtime = 0
prevbuild = 0


def parsing():
    global prevtime
    cb_data = {"timestamp": prevtime, "buildnr": prevbuild}
    try:
        with open("currentbuild.json", "r+") as currentbuild:
            cb_data = json.load(currentbuild)
            prevtime = cb_data["timestamp"]
            response = urllib.urlopen('http://198.23.242.205:8080/job/ForgeEssentials/lastSuccessfulBuild/api/json')
            data = json.load(response)
            if not data["building"] and data["result"] == "SUCCESS":
                if data["timestamp"] > prevtime:
                    print "There is a newer build."
                    cb_data["timestamp"] = data["timestamp"]
                    cb_data["buildnr"] = data["number"]

                    artifactindex = 0
                    for a in data["artifacts"]:
                        if a["fileName"].endswith("-server.zip"):
                            break
                        else:
                            artifactindex += 1
                    print "Downloading..."
                    urllib.urlretrieve(
                        'http://198.23.242.205:8080/job/ForgeEssentials/lastSuccessfulBuild/artifact/build/libs/' +
                        data["artifacts"][artifactindex]["fileName"], data["artifacts"][artifactindex]["fileName"])
                    print "Removing the old..."
                    for f in os.listdir("mods"):
                        if re.search("forgeessentials-.+-servercore.jar", f):
                            os.remove(os.path.join("mods", f))
                    shutil.rmtree(os.path.join("ForgeEssentials", "lib"))
                    shutil.rmtree(os.path.join("ForgeEssentials", "modules"))
                    print "Extractiong the new..."
                    with zipfile.ZipFile(data["artifacts"][artifactindex]["fileName"], "r") as z:
                        z.extractall()

                    currentbuild.seek(0, 0)
                    json.dump(cb_data, currentbuild)
                    print "Finished updating to latest build"
                else:
                    print "Already got latest build."


    except IOError, e:
        if e.filename == "currentbuild.json":
            with open("currentbuild.json", "w") as currentbuild:
                json.dump(cb_data, currentbuild)
            parsing()


parsing()