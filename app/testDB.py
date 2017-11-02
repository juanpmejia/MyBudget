from database import Database

import datetime



db = Database(True)

db.createCategory("juanpam@javerianacali.edu.co","Test")
#db.createUser("Paula", "superpass", "asd@hotmail.com", "1994-08-08", "F")
for i in range(400):
    #db.createIncome(datetime.datetime.now(), 32, "this is just bullshit", "asd@hotmail.com")
    db.createExpense("Test", datetime.datetime.now(), 40, "THIS SUCKS", "juanpam@javerianacali.edu.co")

#db.updateCategory("probando@gmail.com", "Test", totalCost = 28)

#incomes = db.readIncomes("asd@hotmail.com")
#for i in incomes:
#    db.deleteIncome(i["_id"])
#print(db.readUserByEmail("asd@hotmail.com"))
# db.updateUserByEmail("asd@hotmail.com",name="Alopecia")
# print(db.readUserByEmail("asd@hotmail.com"))
# db.deleteUserByEmail("asd@hotmail.com")
# print(db.readUserByEmail("asd@hotmail.com"))
#db.createCategory("asd@hotmail.com", "Gasolina")
#print(db.readCategoriesByUserEmail("asd@hotmail.com"))