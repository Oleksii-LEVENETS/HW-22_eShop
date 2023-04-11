# HW-22_eShop
=====================
1. Runserver (on localhost:8000)

```bash
python3 manage.py migrate
```

```bash
./manage.py loaddata shop/fixtures/users.json
```

```bash
python3 manage.py runserver localhost:8000
```

```bash
celery -A core  worker --loglevel=INFO  -B  
```

```bash
celery -A core --broker=amqp://guest:guest@localhost:5672// flower --port=5555 --basic_auth=admin:admin
```

