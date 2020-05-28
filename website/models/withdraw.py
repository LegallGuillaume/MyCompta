try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

class Withdraw:
    def __init__(self):
        self.money = 0
        self.motif = ''
        self.created = ''
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Withdraw money: '{}'>".format(self.money)

class WithdrawDAO(DbDAO):
    def __init__(self):
        super().__init__('withdraw')
        self.obj_type = Withdraw
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'money': 'INTEGER NOT NULL',
            'motif': 'TEXT',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }