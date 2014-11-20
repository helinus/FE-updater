# FE-updater

**NOTE: the script only works from FE build 223 because of FEs build changes.**

Place FE-updater.py in the same folder as the minecraft jar and then run it whenever you want to update to the latest FE-build.

The python script fetches the latest build data from the [FE Jenkins](http://198.23.242.205:8080/job/ForgeEssentials/) and if there is a newer build then what you have, replaces the modules and core jar leaving configs and perm as they are.

You can at any time see the last build it fetched in ``FEVersion.txt``.
