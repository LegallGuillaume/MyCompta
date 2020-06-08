import unittest
import os
from models.client import ClientDAO, Client
from models.db import DbDAO, DB
from models.insurance import InsuranceDAO, Insurance
from models.invoice import InvoiceDAO, Invoice
from models.profile import ProfileDAO, Profile
from models.quotation.quotation import QuotationDAO, Quotation
from models.quotation.item_quotation import QuotationItemDAO, QuotationItem


class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = None
        directory_test = os.path.abspath('..') + os.sep + 'test_dir'
        os.makedirs(directory_test, exist_ok=True)
        os.mknod(directory_test + os.sep + 'test_db')
        self.db_path = directory_test + os.sep + 'test_db' 
    def testconnection(self):
        self.db = DB(self.db_path)
        self.assertIsNotNone(self.db, msg='Impossible to create db "test_db"')

        self.assertEqual((1 + 2), 3)
        self.assertEqual(0 + 1, 1)
    def testMultiply(self):
        self.assertEqual((0 * 10), 0)
        self.assertEqual((5 * 8), 40)

if __name__ == '__main__':  
    unittest.main()
