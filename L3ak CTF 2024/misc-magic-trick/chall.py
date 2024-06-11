# #!/usr/local/bin/python
# from magika import Magika
# from base64 import b64decode

# inp = b64decode("cHJpbnQoIkhlbGxvLCB3b3JsZCEiKQ==")

# magika = Magika()
# indentification = magika.identify_bytes(inp)
# print(f"{indentification = }\n")

# dl = indentification.dl
# print(f"{dl = }\n")
# output = indentification.output
# print(f"{output= }")
# if dl.ct_label != output.ct_label or dl.score <= 0.99 or output.score <= 0.99 or "python" in output.ct_label:
#     print("Nope.")
#     exit()

# exec(inp, {"__builtins__": None})



#!/usr/local/bin/python
from magika import Magika
from base64 import b64decode

inp = b64decode("cHJpbnQoIkhlbGxvLCB3b3JsZCEpICMgVGhpcyBpcyBhIHNhZmUgcGF5bG9hZA==")

magika = Magika()
indentification = magika.identify_bytes(inp)
print(f"{indentification = }\n")

dl = indentification.dl
print(f"{dl = }\n")
output = indentification.output
print(f"{output= }")
if dl.ct_label != output.ct_label or dl.score <= 0.99 or output.score <= 0.99 or "python" in output.ct_label:
    print("Nope.")
    exit()

exec(inp, {"__builtins__": None})
