# coding=utf-8
from database import Database
from bson.objectid import ObjectId
import datetime



db = Database(False)
#db.createUser("Paula", "superpass", "asd@hotmail.com", "1994-08-08", "F")
for i in range(120):
    pass
    #db.createIncome(datetime.datetime.now(), 32, "this is just bullshit", "juanpam@javerianacali.edu.co")
    #db.createExpense("Test", datetime.datetime.now(), 4000, "I WANNA DIE "+str(i), "juanpam@javerianacali.edu.co")
    #db.createExpense("Jeje", datetime.datetime.now(), 40, "THIS SUCKS", "juanpam@javerianacali.edu.co")


# print(db.readExpenses("C1", groupId = "5a012de1b369205de91af247"))

# groupId = "5a012de1b369205de91af247"
# print(groupId, ObjectId(groupId))

# print(list(db.expensesCollection.find({"groupId" : ObjectId(groupId), "categoryName" : "C1"})))
#db.createGroup("juanpam@javerianacali.edu.co", "Grupo prueba")
#print(db.readGroups("juanpam@javerianacali.edu.co"))

#print(db.readGroupBySubject("GrUpo prueba", "juanpam@javerianacali.edu.co"))
#print(db.readExpenses("Jeje","juanpam@javerianacali.edu.co"))

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