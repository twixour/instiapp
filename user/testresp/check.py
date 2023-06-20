# import requests

# url = 'http://127.0.0.1:8000/user'
# headers = {'Authorization': 'Token 9a6121a8353fc15fa876e2bd7a749e12bf590bca'}

# r =requests.get(url, headers=headers)

# print(r)


import requests

url = 'http://127.0.0.1:8000/user'
headers = {'Authorization': 'Token 4e85ca4604c2dcb856f0970185c7fc6b0efc2e2d'}
r = requests.get(url, headers=headers)
print(r)