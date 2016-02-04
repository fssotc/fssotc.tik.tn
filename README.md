MTCFSS Website
===

That's our official website. It written on python using django and hosted on
Azure.

## Local deployment

First, make sure you have python (>=3.4) and pip installed. Then;
```shell
pip install -r requirement.txt
./manage.py migrate
./manage.py createsuperuser # create your local super user
```

To launch the server:

```shell
./manage.py 0.0.0.0:8080
```

and open http://0.0.0.0:8080 link on your browser
