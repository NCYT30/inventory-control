from peewee import *
from datetime import datetime


database = MySQLDatabase('inventory control',
                         user = 'root',
                         password = 'NCYT30',
                         host = 'localhost',
                         port = 3306)


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


class Category(Model):
    name = CharField(max_length = 30)

    class Meta:
        database = database
        table_name = 'Category'



class Inventory(Model):
    product = CharField(max_length = 25)
    sku = IntegerField()
    ubication = CharField(max_length = 35)
    method = CharField(max_length = 10)
    date = CharField(max_length = 15)
    detail = CharField(max_length = 20)
    amount = IntegerField()
    unit_value = IntegerField()
    fk_category = ForeignKeyField(Category, backref = 'category')
    fk_user = ForeignKeyField(Users, backref = 'user')
    active = IntegerField()
    
    class Meta:
        database = database
        table_name = 'Inventory'




class Sales(Model):
    fk_inv = ForeignKeyField(Inventory, backref = 'inv')
    amount = IntegerField()
    total_value = IntegerField()

    class Meta:
        database = database
        table_name = 'Sales'



class Permissions(Model):
    name = CharField(max_length = 30)

    class Meta:
        database = database
        table_name = 'Permissions'


class RolPer(Model):
    fk_per = ForeignKeyField(Permissions, backref = 'per')
    fk_user = ForeignKeyField(Users, backref = 'user')

    class Meta:
        database = database
        table_name = 'RolPer'



class Providers(Model):
    name = CharField(max_length = 25)
    description = CharField(max_length = 50)
    addres = CharField(max_length = 30)
    email = CharField(max_length = 30)
    phone = IntegerField()
    fkusr = ForeignKeyField(Users, backref = 'users')
    active = IntegerField()

    class Meta:
        database = database
        table_name = 'Providers'
        