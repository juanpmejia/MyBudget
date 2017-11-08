def getMessage():
    file = open("app/static/message.txt", "r")
    return str(file.read())
    
def getSignature():
    file = open("app/static/signature.txt", "r")
    return str(file.read())