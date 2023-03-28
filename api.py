import requests


endpoint_1 = "http://localhost:8000/eshop_api/products/"

endpoint_2 = "http://localhost:8000/eshop_api/orderitems/"

endpoint_3 = "http://localhost:8000/eshop_api/orders/"

headers = {"Authorization": "Token 72604ae7455bdd36e535e5cb171c6cfbcc25e128"}

get_response_1 = requests.get(endpoint_1, headers=headers)
get_response_2 = requests.get(endpoint_2, headers=headers)
get_response_3 = requests.get(endpoint_3, headers=headers)


print("get_response_1: ", get_response_1.json())
print("#"*50)
print("get_response_2: ", get_response_2.json())
print("#"*50)
print("get_response_3: ", get_response_3.json())
