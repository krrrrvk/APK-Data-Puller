# APK-data-puller

Simple python script that pulls all apk data from the `/data/data/` folder such as `shared_prefs`,`databases`, `files` etc.

## Installation 
Clone repository
```bash
$ git clone https://github.com/krrrrvk/APK-data-puller.git
```
Install neccessary requirements
```bash
$ pip3 install -r requirements.txt
```

## Basic usage

```bash
$ python3 datapuller.py
usage: datapuller.py [-h] [-p PACKAGE] [-u UPDATE] [-l]

Pull all apk data

options:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        Package name
  -u UPDATE, --update UPDATE
                        Update package data
  -l, --list            List all packages
```

### List all packages

```bash
$ python3 datapuller.py -l

[+] Listing all available packages:
android
android.auto_generated_rro_vendor__
android.autoinstalls.config.samsung
com.android.apps.tag
com.android.backupconfirm
com.android.bips
com.android.bluetooth
com.android.bluetoothmidiservice
com.android.bookmarkprovider
com.android.calllogbackup
com.android.carrierconfig
com.android.carrierdefaultapp
com.android.cellbroadcastreceiver
com.android.cellbroadcastservice
com.android.certinstaller
com.android.chrome
com.android.companiondevicemanager
com.android.cts.ctsshim
com.android.cts.priv.ctsshim
com.android.dreams.basic
com.android.dreams.phototable
com.android.dynsystem
com.android.egg

...
..
.

```

### Pull specific package data 

Script creates `projects` folder which contains all of the pulled packages and their data

```bash
$ python3 datapuller.py -p com.android.settings
[+] Devices:
Device

[+] Package info:  {'version_name': '11', 'version_code': '29', 'signature': '3c0fc89 version:2, signatures:[b378e95c], past signatures:[]'}

[+] The package 'com.android.settings' exists in /data/data. Pulling now...

[+] Folder does not exist. Creating new projects folder at location '/APK-data-puller/projects'

[+] Folder does not exist. Creating new project at location '/APK-data-puller/projects/com.android.settings'
/sdcard/cache/: 35 files pulled, 0 skipped. 7.8 MB/s (2383917 bytes in 0.291s)
/sdcard/code_cache/: 0 files pulled, 0 skipped.

[+] Directories pulled:
cache
code_cache

```

### Push modified data
```bash
$ python3 datapuller.py -u com.android.settings
[+] Pushing changes please wait.
/APK-data-puller/projects/com.android.setti...s/: 35 files pushed, 0 skipped. 2.4 MB/s (2383917 bytes in 0.951s)
```


