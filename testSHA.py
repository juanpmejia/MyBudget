import hashlib

m = hashlib.sha256()
test = "This is a motherfucking mega test YOU BITCHES!".encode('utf-8')
m.update(test)
print(m.hexdigest())
