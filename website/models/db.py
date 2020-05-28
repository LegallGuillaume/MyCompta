import sqlite3
from datetime import datetime
try:
    from settings.config import DB_PATH
except ModuleNotFoundError:
    from website.settings.config import DB_PATH

class DB:
    def __init__(self):
        self.conn = None
    def connect(self):
        self.conn = sqlite3.connect(DB_PATH)
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()
    def get_con(self):
        if not self.conn:
            self.connect()
        return self.conn


class DbDAO:
    def __init__(self, table_name):
        self.__tablename = table_name
        self.obj_type = type(self)
        self.__db = DB()

    def get_table_name(self):
        return self.__tablename

    def where(self, col, value):
        if isinstance(value, str):
            value = "'" + value + "'"
        return '{} = {}'.format(col, value)

    def close(self):
        self.__db.get_con().close()

    def create_table(self):
        if not hasattr(self, 'table_create'):
            return False
        a_t_c = getattr(self, 'table_create')
        table_create = [ '{} {}'.format(x, a_t_c[x]) for x in a_t_c]
        __sql = """ CREATE TABLE IF NOT EXISTS {} ( {} )""".format(
            self.__tablename, ', '.join(table_create)
        )
        try:
            conn = self.__db.get_con()
            conn.execute(__sql)
            conn.commit()
            return True
        except Exception as e:
            print('DB create table ERROR:', e)
            return False

    def exist(self, where):
        if not issubclass(type(self), DbDAO):
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)

        sql = """ SELECT * FROM {} WHERE {}""".format(self.__tablename, wh)
        try:
            conn = self.__db.get_con()
            cursor = conn.cursor()
            cursor.execute(sql)
            if len(cursor.fetchall()) > 0:
                return True
        except Exception as e:
            print('DB exist ERROR:', e)
        return False

    def insert(self, obj):
        """
        INSERT INTO TABLE_NAME [(column1, column2, column3,...columnN)]  
        VALUES (value1, value2, value3,...valueN);
        """
        if not issubclass(type(self), DbDAO):
            return False
        dict_class = obj.__dict__
        if 'table_create' in dict_class.keys():
            del dict_class['table_create']
        if 'id' in dict_class.keys():
            del dict_class['id']
        if '_DbDAO__tablename' in dict_class.keys():
            del dict_class['_DbDAO__tablename']
        date_today = datetime.now().strftime('%d/%m/%Y')
        setattr(obj, 'created', date_today)
        columnN = ', '.join(list(dict_class.keys()))
        values = [ str("'" + x + "'") if isinstance(x, str) else str(x) for x in list(dict_class.values())]
        valueN = ', '.join(values)

        sql = """ INSERT INTO {} ( {} ) VALUES ( {} )""".format(self.__tablename, columnN, valueN)
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print('DB insert ERROR:', e)
            return False
        
    def update(self, obj, where):
        """
        UPDATE table_name
        SET column1 = value1, column2 = value2...., columnN = valueN
        WHERE [condition];
        """
        if not issubclass(type(self), DbDAO):
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)
        dict_class = obj.__dict__
        if 'table_create' in dict_class.keys():
            del dict_class['table_create']
        if 'id' in dict_class.keys():
            del dict_class['id']
        if '_DbDAO__tablename' in dict_class.keys():
            del dict_class['_DbDAO__tablename']
        col_value = [ '{} = {}'.format(x, str( "'" + dict_class[x] + "'") if isinstance(dict_class[x], str) else str(dict_class[x])) for x in dict_class]
        sql = """ UPDATE {} SET {} WHERE {} """.format(self.__tablename, ','.join(col_value), wh)
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print('DB update ERROR:', e)
            return False

    def __construct_obj(self, cols_name, result, where):
        if len(cols_name) != len(result):
            raise Exception('Not object found with : ' + where)
        obj = self.obj_type()
        # remove attr from parent
        try:
            del obj._DbDAO__tablename
            del obj._DbDAO__type
            del obj._DbDAO__db
            del obj.table_create
        except:
            pass
        # set new attr
        for index, col in enumerate(cols_name):
            setattr(obj, col, result[index])
        return obj

    def get(self, where=None):
        if not issubclass(type(self), DbDAO):
            return
        conn = self.__db.get_con()
        cursor = conn.cursor()
        wh = ''
        if not where:
            pass
        elif isinstance(where, str):
            wh = 'WHERE ' + where
        else: # list
            wh = 'WHERE ' + ' AND '.join(where)
        sql = """ SELECT * FROM {} {}""".format(self.__tablename, wh)
        try:
            cursor.execute(sql)
        except:
            raise Exception('Not object found with : ' + where)
        cols_name = list(map(lambda x: x[0], cursor.description))
        results = list(cursor.fetchall())
        list_obj = list()
        for result in results:
            list_obj.append(self.__construct_obj(cols_name, result, where))
        return list_obj

    def delete(self, where):
        """
        DELETE FROM table_name
        WHERE [condition];
        """
        if not issubclass(type(self), DbDAO):
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)
            
        sql = """ DELETE FROM {} WHERE {}""".format(self.__tablename, wh)
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print('DB ERROR:', e)
            return False

    def drop(self, valid1, valid2):
        if not issubclass(type(self), DbDAO) and valid1 and valid2:
            return list()
            
        sql = """ DROP TABLE {}""".format(self.__tablename)
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print('DB drop ERROR:', e)
            return False

    def field(self, where, col):
        if not issubclass(type(self), DbDAO):
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)
            
        sql = """ SELECT {} FROM {} WHERE {}""".format(col, self.__tablename, wh)
        try:
            conn = self.__db.get_con()
            cursor = conn.cursor()
            cursor.execute(sql)
            results = list(cursor.fetchall())
            return results
        except Exception as e:
            print('DB ERROR:', e)
            return list()

    def __exit__(self):
        self.close()