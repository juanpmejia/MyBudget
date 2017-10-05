from database import Database

import datetime



db = Database(False)
#db.createUser("Paula", "superpass", "asd@hotmail.com", "08-08-1994", "F")
print(db.readUserByName("asd@hotmail.com"))
print(db.readUserById("59d57ba1b36920361b3078c8"))
