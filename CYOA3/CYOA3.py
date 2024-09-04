import base64
 
def b64_encode(s:str) -> str:
    encoded = base64.b64encode(s.encode("ascii")).decode("ascii")
    return encoded
 
def b64_decode(s:str) -> str:
    decoded = base64.b64decode(s.encode("ascii")).decode("ascii")
    return decoded

print(b64_encode(input("Encode: ")))
print(b64_decode(input("Decode: ")))