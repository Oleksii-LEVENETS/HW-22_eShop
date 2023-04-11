# HW-22_eStorehouse  
===================  
1. Fixtures and runserver (on localhost:8001)  
```bash
python3 manage.py migrate
```
# Option_1  
```bash
./manage.py create_new_models  
```
```bash
./manage.py loaddata storehouse/fixtures/users.json
```

or  

# Option_2  
```bash
./manage.py loaddata storehouse/fixtures/fresh_db.json
```

```bash
python3 manage.py runserver localhost:8001
```

2. drf-spectacular  
    Sane and flexible OpenAPI 3.0 schema generation for Django REST framework.  
```bash
./manage.py spectacular --color --file schema.yml
```
See /schema.yml  

# Optional UI:  
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")   
http://localhost:8001/api/schema/swagger-ui/#/  

    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc")  
http://localhost:8001/api/schema/redoc/  
