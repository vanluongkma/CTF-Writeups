from base64 import b64decode

encrypt = "U2VjdXJpbmV0c3tCQVNFNjRJU0ZPUlNVUkVJU1NPTUVUSElOR30="
flag = b64decode(encrypt).decode()
print(flag)
# Securinets{BASE64ISFORSUREISSOMETHING}
