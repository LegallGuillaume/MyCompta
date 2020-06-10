try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
from hashlib import sha256

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Profile:
    def __init__(self):
        self.name = ''
        self.prenom = ''
        self.password = ''
        self.adresse = ''
        self.comp_adresse = ''
        self.cp = ''
        self.ville = ''
        self.pays = ''
        self.siret = ''
        self.tel = ''
        self.email = ''
        self.created = ''

    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Profile nom: '{}' prenom: '{}'>".format(self.name, self.prenom)

    def __setattr__(self, name, value):
        if name == 'password' and len(value) != 64:
            value = sha256(str(value).encode(encoding='utf-8')).hexdigest()
        object.__setattr__(self, name, value)

class ProfileDAO(DbDAO):
    def __init__(self, dbpath=None):
        super().__init__('profile', db_path=dbpath)
        self.obj_type = Profile
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'name': 'TEXT NOT NULL',
            'prenom': 'TEXT NOT NULL',
            'password': 'TEXT',
            'adresse': 'TEXT',
            'comp_adresse': 'TEXT',
            'cp': 'TEXT',
            'ville': 'TEXT',
            'pays': 'TEXT',
            'siret': 'TEXT UNIQUE',
            'tel': 'TEXT',
            'email': 'TEXT',
            'created': 'TEXT'
        }
    
    def check_auth(self, where, password):
        result = self.field(where, 'password')
        hash = sha256(str(password).encode(encoding='utf-8')).hexdigest()
        if result:
            if result[0][0] == hash:
                return True
        return False

    def get_profile_id(self, _where):
        result = self.field(_where, 'id')
        if result:
            return result[0][0]
        return -1

    def get_list_profile(self):
        return self.get()

    def exist(self, obj):
        if isinstance(obj, Profile):
            if hasattr(obj, 'id'):
                return super().exist(self.where('id', obj.id))
            else:
                return super().exist(self.where('siret', obj.siret))
        else:
            return super().exist(obj)
    def update(self, obj):
        if hasattr(obj, 'id'):
            return super().update(obj, self.where('id', obj.id))
        else:
            return super().update(obj, self.where('siret', obj.siret))
    def delete(self, obj):
        if isinstance(obj, Profile):
            if hasattr(obj, 'id'):
                return super().delete(self.where('id', obj.id))
            else:
                return super().delete(self.where('siret', obj.siret))
        else:
            return super().delete(obj)
