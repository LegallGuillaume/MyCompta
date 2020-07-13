try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
from hashlib import sha256
import logging

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

class Profile:
    def __init__(self):
        self.name = ''
        self.firstname = ''
        self.password = ''
        self.address = ''
        self.comp_address = ''
        self.zipcode = ''
        self.city = ''
        self.country = ''
        self.siret = ''
        self.phone = ''
        self.email = ''
        self.created = ''

    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Profile lastname: '{}' firstname: '{}'>".format(self.name, self.firstname)

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
            'firstname': 'TEXT NOT NULL',
            'password': 'TEXT',
            'address': 'TEXT',
            'comp_address': 'TEXT',
            'zipcode': 'TEXT',
            'city': 'TEXT',
            'country': 'TEXT',
            'siret': 'TEXT UNIQUE',
            'phone': 'TEXT',
            'email': 'TEXT',
            'created': 'TEXT'
        }
    
    def check_auth(self, where_or_obj, password):
        if isinstance(where_or_obj, Profile):
            hash = sha256(str(password).encode(encoding='utf-8')).hexdigest()
            return (where_or_obj.password == hash)
        result = self.field(where_or_obj, 'password')
        hash = sha256(str(password).encode(encoding='utf-8')).hexdigest()
        if result:
            return (result[0][0] == hash)
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
                logging.info('ProfileDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('ProfileDAO use exist with siret')
                return super().exist(self.where('siret', obj.siret))
        else:
            logging.info('ProfileDAO use delete with WHERE')
            return super().exist(obj)
    def update(self, obj):
        if hasattr(obj, 'id'):
            logging.info('ProfileDAO use update with id')
            return super().update(obj, self.where('id', obj.id))
        else:
            logging.info('ProfileDAO use update with siret')
            return super().update(obj, self.where('siret', obj.siret))
    def update(self, obj, where):
        logging.info('ProfileDAO use update')
        return super().update(obj, where)
    def delete(self, obj):
        if isinstance(obj, Profile):
            if hasattr(obj, 'id'):
                logging.info('ProfileDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('ProfileDAO use delete with siret')
                return super().delete(self.where('siret', obj.siret))
        else:
            logging.info('ProfileDAO use delete with WHERE')
            return super().delete(obj)
