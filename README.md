# basic_localhost_django

## installation instruction

```bash
python3 -m pip install Django

```
then go to project root directory, then run the following commands in order

```bash

python3 manage.py migrate

python3 manage.py runserver

```

```bash

pip3 install locust

```

### run locust load testing

```bash

locust -f locusfile.py --host http://127.0.0.1:8000

````

### locust run headless
```bash
 locust -f locustfile.py --headless -u 1000 -r 100
 
 it is possible to set a time limit too
 locust -f --headless -u 1000 -r 100 --run-time 1h30m
```

###### side note: that was a Django localhost

#### All somewhat depend on your system configuration tho
