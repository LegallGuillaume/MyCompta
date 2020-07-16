import sqlite3
from datetime import datetime
import logging
try:
    from settings.config import DB_PATH
except ModuleNotFoundError:
    from website.settings.config import DB_PATH

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

class DB:
    def __init__(self, db_path):
        self.conn = None
        self.dbpath = db_path if db_path else DB_PATH
        logging.debug("DB path: " + self.dbpath)
    def connect(self):
        self.conn = sqlite3.connect(self.dbpath)
        logging.debug('DB connect: ' + str(self.conn is not None))
    def commit(self):
        self.conn.commit()
        logging.debug("DB commit OK")
    def close(self):
        self.conn.close()
        self.conn = None
        logging.debug("DB close")
    def get_con(self):
        if not self.conn:
            self.connect()
        return self.conn


class DbDAO:
    def __init__(self, table_name, db_path=DB_PATH):
        self.__tablename = table_name
        self.obj_type = type(self)
        self.__db = DB(db_path)
        logging.info('Create DbDAO with db path: ' + str(db_path))

    def get_table_name(self):
        logging.info('get_table_name: ' + self.__tablename)
        return self.__tablename

    def where(self, col, value):
        if isinstance(value, str):
            value = "'" + value + "'"
        return '{} = {}'.format(col, value)

    def close(self):
        logging.info('DbDAO use close')
        self.__db.get_con().close()

    def create_table(self):
        logging.info('DbDAO use create_table')
        if not hasattr(self, 'table_create'):
            logging.debug('DbDAO not attribute table_create')
            return False
        a_t_c = getattr(self, 'table_create')
        table_create = [ '{} {}'.format(x, a_t_c[x]) for x in a_t_c]
        __sql = """ CREATE TABLE IF NOT EXISTS {} ( {} )""".format(
            self.__tablename, ', '.join(table_create)
        )
        logging.debug('DbDAO create_table sql: "' + __sql +'"')
        try:
            conn = self.__db.get_con()
            conn.execute(__sql)
            conn.commit()
            logging.info('DbDAO create_table OK')
            return True
        except Exception as e:
            logging.error('DbDAO create_table FAILED "' + str(e) + '"')
            return False

    def exist(self, where):
        logging.info('DbDAO use exist with "' + str(where) + '"')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO exist is use in non object DbDAO')
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)

        sql = """ SELECT * FROM {} WHERE {}""".format(self.__tablename, wh)
        logging.debug('DbDAO exist sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            cursor = conn.cursor()
            cursor.execute(sql)
            if len(cursor.fetchall()) > 0:
                logging.info('DbDAO exist OK')
                return True
        except Exception as e:
            logging.error('DbDAO exist FAILED "' + str(e) + '"')
        return False

    def insert(self, obj):
        """
        INSERT INTO TABLE_NAME [(column1, column2, column3,...columnN)]  
        VALUES (value1, value2, value3,...valueN);
        """
        logging.info('DbDAO use update')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO insert is use in non object DbDAO')
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
        logging.debug('DB insert sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            cursor = conn.cursor()
            cursor.execute(sql)
            obj.id = cursor.lastrowid
            conn.commit()
            logging.info('DbDAO insert OK')
            return True
        except Exception as e:
            logging.error('DbDAO insert FAILED "' + str(e) + '"')
            return False
        
    def update(self, obj, where):
        """
        UPDATE table_name
        SET column1 = value1, column2 = value2...., columnN = valueN
        WHERE [condition];
        """
        logging.info('DbDAO use update with "' + str(where) + '"')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO update is use in non object DbDAO')
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
        logging.debug('DB update sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            logging.info('DbDAO update OK')
            return True
        except Exception as e:
            logging.error('DbDAO update FAILED "' + str(e) + '"')
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
            logging.warning('DbDAO __contruct_obj cannot del some default attribute')
        # set new attr
        for index, col in enumerate(cols_name):
            setattr(obj, col, result[index])
        return obj

    def get(self, where=None):
        logging.info('DbDAO use get with "' + str(where) + '"')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO get is use in non object DbDAO')
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
        logging.debug('DB get sql: "' + sql +'"')
        try:
            cursor.execute(sql)
            logging.info('DbDAO get OK')
        except:
            logging.error('DbDAO get failed')
            raise Exception('Not object found with : ' + where)
        cols_name = list(map(lambda x: x[0], cursor.description))
        results = list(cursor.fetchall())
        list_obj = []
        for result in results:
            list_obj.append(self.__construct_obj(cols_name, result, where))
        return list_obj

    def delete(self, where):
        """
        DELETE FROM table_name
        WHERE [condition];
        """
        logging.info('DbDAO use delete with "' + str(where) + '"')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO delete is use in non object DbDAO')
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)
            
        sql = """ DELETE FROM {} WHERE {}""".format(self.__tablename, wh)
        logging.debug('DB delete sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            logging.info('DbDAO delete OK')
            return True
        except Exception as e:
            logging.error('DbDAO delete FAILED "' + str(e) + '"')
            return False

    def drop(self, valid1, valid2):
        logging.info('DbDAO use drop')
        if not issubclass(type(self), DbDAO) or not valid1 or not valid2:
            logging.debug('DbDAO drop is not valid argument')
            return False

        sql = """ DROP TABLE {}""".format(self.__tablename)
        logging.debug('DB drop sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            conn.execute(sql)
            conn.commit()
            logging.info('DbDAO drop OK')
            return True
        except Exception as e:
            logging.error('DbDAO drop FAILED "' + str(e) + '"')
            return False

    def field(self, where, col):
        logging.info('DbDAO use field with WHERE = "' + str(where) + '", COL = "' + col + '"')
        if not issubclass(type(self), DbDAO):
            logging.debug('DbDAO field is use in non object DbDAO')
            return False
        wh = ''
        if isinstance(where, str):
            wh = where
        else: # list
            wh = ' AND '.join(where)
            
        sql = """ SELECT {} FROM {} WHERE {}""".format(col, self.__tablename, wh)
        logging.debug('DB field sql: "' + sql +'"')
        try:
            conn = self.__db.get_con()
            cursor = conn.cursor()
            cursor.execute(sql)
            results = list(cursor.fetchall())
            logging.info('DbDAO field OK')
            return results
        except Exception as e:
            logging.error('DbDAO field FAILED "' + str(e) + '"')
            return list()

    def colnames(self):
        conn = self.__db.get_con()
        cursor = conn.execute('select * from {}'.format(self.__tablename))
        names = list(map(lambda x: x[0], cursor.description))
        return (self.__tablename, names)

    def __exit__(self):
        logging.info('DbDAO __exit__ OK')
        self.close()