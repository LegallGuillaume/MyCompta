try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Client:
    def __init__(self):
        self.name = ''
        self.adresse = ''
        self.comp_adresse = ''
        self.cp = ''
        self.ville = ''
        self.pays = ''
        self.created = ''
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Client name: '{}'>".format(self.name)

class ClientDAO(DbDAO):
    def __init__(self):
        super().__init__('client')
        self.obj_type = Client
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'name': 'TEXT NOT NULL',
            'adresse': 'TEXT',
            'comp_adresse': 'TEXT',
            'cp': 'TEXT',
            'ville': 'TEXT',
            'pays': 'TEXT',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }
    
    def exist(self, obj):
        if isinstance(obj, Client):
            if hasattr(obj, 'id'):
                return super().exist(self.where('id', obj.id))
            else:
                return super().exist(self.where('name', obj.name))
        else:
            return super().exist(obj)
    def update(self, obj):
        if hasattr(obj, 'id'):
            return super().update(obj, self.where('id', obj.id))
        else:
            return super().update(obj, self.where('name', obj.name))
    def delete(self, obj):
        if isinstance(obj, Client):
            if hasattr(obj, 'id'):
                return super().delete(self.where('id', obj.id))
            else:
                return super().delete(self.where('name', obj.name))
        else:
            return super().delete(obj)