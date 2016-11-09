Fss Open Tech Club Website
===
[![Build
Status](https://travis-ci.org/fssotc/website.svg?branch=master)](https://travis-ci.org/fssotc/website)
[![Stories in
Ready](https://badge.waffle.io/fssotc/website.svg?label=ready&title=Ready)](http://waffle.io/fssotc/website)

That's our official website. It's written on python using django and hosted on
Azure.

## Local deployment

First, make sure you have python (>=3.4) and pip installed. Then;
```shell
pip install -r requirement.txt
./manage.py migrate
./manage.py createsuperuser # create your local super user
```

To launch the server, run

```shell
./manage.py 0.0.0.0:8080
```

and open http://0.0.0.0:8080 link on your browser

## Work flow

For project directory structure, read [Description](#description) section.

All dev is done on master branch. Stable code is then merged to azure branch
where the official deployed site is kept on sync.

Please send patches only to the master branch.

## Description
- `project/`: django project folder
- `db/`: Database models app
- `website/`: main website app
- `deploy.py`: python script to generate and load local secret key
- `deploy.cmd`: Azure (ISS) specific deployment script run on every code change
- `manage.py`: well, just django generated management script
- `ptvs_virtualenv_proxy.py`: Visual Studio Python Tools generated script
- `requirements.txt`: project required packages
- `runtime.txt`: Azure specific file to set python runtime version
- `setup.py`: easy_install script
- `web.3.4.config`: Azure (IIS) configuration file
- `.deployment`: Azure (IIS) specific file to set `deploy.cmd` file path
- `test_settings.py`: django-setuptest specific setting file for setuptools
  testing support
