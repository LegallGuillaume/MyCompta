try:
    from models.db import DbDAO
    from models.devis.item_devis import DevisItem, DevisItemDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
    from website.models.devis.item_devis import DevisItem, DevisItemDAO

class Devis:
    def __init__(self):
        self.numero = -1
        self.date_envoi = ''
        self.date_validite = ''
        self.client = ''
        self.id_profile = -1
        self.total = 0.0
        self.tva_price = 0.0
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Devis N°{}>".format(self.numero)

    def add_item(self, item):
        if not isinstance(item, DevisItem):
            return
        if not hasattr(self, 'list_item'):
            self.list_item = list()
        item.id_devis = self.id
        new_price = (item.quantity*item.unit_price)
        if not item.reduction:
            self.total += new_price
        else:
            self.total = max(0, self.total-new_price)
        self.list_item.append(item)

class DevisDAO(DbDAO):
    def __init__(self):
        super().__init__('devis')
        self.obj_type = Devis
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'numero': 'INTEGER NOT NULL',
            'total': 'FLOAT NOT NULL',
            'tva_price': 'FLOAT NOT NULL',
            'client': 'TEXT NOT NULL',
            'date_validite': 'TEXT NOT NULL',
            'date_envoi': 'TEXT NOT NULL',
            'created': 'TEXT NOT NULL',
            'id_profile': 'INTEGER NOT NULL'
        }

    def get(self, where=None):
        obj = super().get(where)
        for o in obj:
            itemdao = DevisItemDAO()
            o.list_item = itemdao.get(itemdao.where('id_devis', o.id))
        return obj

    def insert(self, obj):
        list_item = list()
        if hasattr(obj, 'list_item'):
            list_item = obj.list_item
            del obj.list_item
        itemdao = DevisItemDAO()
        for item in list_item:
            item.id_devis = self.id
            itemdao.insert(item)
        return super().insert(obj)

    def update(self, obj, where):
        list_item = obj.list_item
        del obj.list_item
        ret = super().update(obj, where)
        obj.list_item = list_item
        return ret