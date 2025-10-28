import requests

# Test the auth endpoint
response = requests.get("http://127.0.0.1:8000/auth/")
print("Auth endpoint response:", response.text)
print("Status code:", response.status_code)

# Test the docs endpoint
response = requests.get("http://127.0.0.1:8000/docs")
print("Docs endpoint status code:", response.status_code)