'''
Created on Nov 6, 2013

@author: Erik
'''
import unittest
from node import Node
from node import FactorNode
from node import VariableNode
from communication.message import BinaryMessage


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_connections(self):
        a = Node()
        b = Node()
        a.add_directed_connection(b)
        self.assertIn(b, a.connections)
        self.assertNotIn(a, b.connections)
        a.add_undirected_connection(b)
        self.assertIn(a, b.connections)
        self.assertEquals(len(a.connections), 1)
        
    def test_factornode_message_generation_BEC(self):
        f1 = FactorNode()
        m1 = BinaryMessage(1, 'a')
        m2 = BinaryMessage(-1, 'b')
        m3 = BinaryMessage(0, 'c')
        
        f1._recieve_message(m1)
        f1._recieve_message(m2)
        f1._recieve_message(m3)
        
        b1 = f1.generate_BEC_message_for('a')
        b2 = f1.generate_BEC_message_for('b')
        b3 = f1.generate_BEC_message_for('c')
        
        self.assertEquals(0, b1.data)
        self.assertEquals(0, b2.data)
        self.assertEquals(-1, b3.data)
        
    def test_variablenode_message_generation_BEC(self):
        v1 = VariableNode()
        v1.recieved_value = 0
        m1 = BinaryMessage(1, 'a')
        m2 = BinaryMessage(0, 'b')
        
        v1._recieve_message(m1)
        v1._recieve_message(m2)
        
        b1 = v1.generate_BEC_message_for('a')
        b2 = v1.generate_BEC_message_for('b')
        
        self.assertEquals(0, b1.data)
        self.assertEquals(1, b2.data)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()