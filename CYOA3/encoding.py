def decode(user:str, encoded:str) -> str:
    key = 0
    data = ''
    for c in user:
        key += ord(c)
    for letter in encoded:
        data += chr(ord(letter) - key)
    return data

def encode(user:str, data:str) -> str:
    #Finding out user key
    key = 0
    datum = ''
    for c in user:
        key += ord(c)
    for letter in data:
        datum += chr(ord(letter) + key)        
    return datum
        
user = 'oaiefhoaihfiaoc'
code = encode(user, 'chinerman')
print(code)
d = decode(user, code)
print(d)