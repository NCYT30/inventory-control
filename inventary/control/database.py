from peewee import *
from datetime import datetime


database = MySQLDatabase('inventory control',
                         user = 'root',
                         password = 'NCYT30',
                         host = 'localhost',
                         port = 3306)




class Inventory(Model):
    product = CharField(max_length = 25)
    sku = IntegerField()
    ubication = CharField(max_length = 35)
    method = CharField(max_length = 10)
    date = CharField(max_length = 15)
    detail = CharField(max_length = 20)
    amount = IntegerField()
    unit_value = IntegerField()
    total_value = IntegerField()
    active = IntegerField()
    
    class Meta:
        database = database
        table_name = 'Inventory'




class Users(Model):
    name = CharField(max_length = 25)
    surnames = CharField(max_length = 25)
    phone = IntegerField()
    email = CharField(max_length = 30)
    password = CharField(max_length = 512)
    active = IntegerField()

    class Meta:
        database = database
        table_name = 'Users'


class Providers(Model):
    id = IntegerField(primary_key = True, index = True)
    name = CharField(max_length = 25)
    description = CharField(max_length = 50)
    addres = CharField(max_length = 30)
    email = CharField(max_length = 30)
    phone = IntegerField()
    active = IntegerField()

    class Meta:
        database = database
        table_name = 'Providers'