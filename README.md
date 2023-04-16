# HW-22_eShop  
=====================
1. Only "eshop" (localhost version):  
https://github.com/Oleksii-LEVENETS/HW-22_eShop/tree/main  

2. Only "estorehouse" (localhost version):    
https://github.com/Oleksii-LEVENETS/HW-22_eStorehouse  

3. Here:  
- Docker
```bash
docker-compose -f docker-compose.yml up -d --build
```
```bash
docker-compose -f docker-compose.yml down -v
```

- estorehouse  http://localhost:8001/    

- eshop  http://localhost/   

- pgAdmin4   http://localhost:5050  (admin@example.com, admin)   

- flower   http://localhost:5555/   

- mailhog   http://localhost:8025/   

- drf-spectacular    
    Sane and flexible OpenAPI 3.0 schema generation for Django REST framework.
See /schema.yml  
# Optional UI:  
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")   
http://localhost:8001/api/schema/swagger-ui/#/  

    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc")  
http://localhost:8001/api/schema/redoc/  


