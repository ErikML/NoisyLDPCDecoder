'''
Created on Nov 6, 2013

@author: Erik
'''
import unittest
from message import Mailbox
from message import Message

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMailBox(self):
        a = Message(1, 'a')
        b = Message(2, 'b')
        c = Message(3, 'c')
        
        mailbox = Mailbox()
        mailbox.recieve_message(a)
        mailbox.recieve_message(b)
        mailbox.recieve_message(c)
        
        nota = mailbox.all_data_except_from('a')
        self.assertIn(2, nota)
        self.assertIn(3, nota)
        self.assertNotIn(1, nota)
        self.assertEqual(len(nota), 2)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMailBox']
    unittest.main()