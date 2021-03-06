#!/usr/bin/env python

# Put this Python 2.7.5 file in the same folder as your minecraft jar.

# Only if there's a newer build will it download the server zip file.
# When run it fetches the latest build timestamp and compares it to
# that of the build it downloaded last and after that it removes the
# old core, modules and libs and extracts the new ones.

versionfile = "FEVersion.txt"

import json
import shutil
import urllib
import re
import os
import sys

def reporthook(count, blockSize, totalSize):
    prevpercent = 0
    percent = int(count * blockSize * 100 / totalSize)
    if percent > prevpercent:
        sys.stdout.write("\r%d%%" % percent + ' complete')
        sys.stdout.flush()
        prevpercent = percent
    if percent == 100:
        sys.stdout.write("\n")

def parsing():
    global prevtime
    global prevbuild
    global cb_data
    prevtime = 0
    prevbuild = 0
    cb_data = ["# The UNIX timestamp and build number\n", "# of the currently used FE version.\n",
               "timestamp: " + str(prevtime)+"\n", "buildnr: " + str(prevbuild)+"\n"]
    try:
        with open(versionfile, "r+") as currentbuild:
            cb_data = currentbuild.readlines()
            prevtime = int(re.search("\d+", cb_data[2]).group(0))
            prevbuild = int(re.search("\d+", cb_data[3]).group(0))
            response = urllib.urlopen('http://ci.forgeessentials.com/job/FE/lastSuccessfulBuild/api/json')
            data = json.load(response)
            if not data["building"] and data["result"] == "SUCCESS":
                if data["timestamp"] > prevtime:
                    print "Latest build is " + str(data["number"]-prevbuild) + " builds ahead of your current one"

                    artifactindex = 0
                    for a in data["artifacts"]:
                        if a["fileName"].endswith("-server.jar"):
                            break
                        else:
                            artifactindex += 1

                    print "Removing the old..."
                    for f in os.listdir("mods"):
                        if re.search("forgeessentials-.+-server.jar", f):
                            os.remove(os.path.join("mods", f))
                    shutil.rmtree(os.path.join("ForgeEssentials", "lib"))

                    print "Downloading the new..."
                    urllib.urlretrieve(
                        'http://bzeutzheim.de:8080/job/ForgeEssentials/'+str(data["number"])+'/artifact/build/libs/' +
                        data["artifacts"][artifactindex]["fileName"], os.path.join("mods", data["artifacts"][artifactindex]["fileName"]), reporthook=reporthook)

                    prevtime = data["timestamp"]
                    prevbuild = data["number"]

                    currentbuild.seek(0, 0)
                    cb_data[2] = "timestamp: " + str(prevtime)+"\n"
                    cb_data[3] = "buildnr: " + str(prevbuild)+"\n"
                    currentbuild.writelines(cb_data)
                    print "Finished updating to build " + str(prevbuild) + "."
                else:
                    print "You already have the latest build."


    except IOError, e:
        if e.filename == versionfile:
            with open(versionfile, "w") as currentbuild:
                currentbuild.writelines(cb_data)
            parsing()

parsing()
