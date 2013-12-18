'''
Created on Nov 6, 2013

@author: Erik
'''
from communication.message import Mailbox
from communication.message import BinaryMessage
from random import random

class Node(object):
    
    def __init__(self, name=None):
        self._connections = set()
        self._name = name
        
    def add_directed_connection(self, other_node):
        if other_node not in self._connections:
            self._connections.add(other_node)
            
    def add_undirected_connection(self, other_node):
        self.add_directed_connection(other_node)
        other_node.add_directed_connection(self)
        
    @property
    def connections(self):
        return self._connections
    
    @property
    def name(self):
        if self._name == None:
            label = str(id(self))
        else:
            label = self._name
        return label
    
    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + self.name + ') connections:' + self.connection_str() + '>'
    
    def connection_str(self):
        s = '{'
        delimeter = ', '
        connections = sorted(list(self._connections))
        for node in connections:
            s += node.short_str() + delimeter
        s = s[:-len(delimeter)]
        s += '}'
        return s
    
    def short_str(self):
        return self.__class__.__name__ + '(' + self.name + ')'
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __le__(self, other):
        return self.name <= other.name
    
    def __eq__(self, other):
        return self is other.name
    
    def __ne__(self, other):
        return self is not other.name
    
    def __gt__(self, other):
        return self.name > other.name
    
    def __ge__(self, other):
        return self.name >= self.other
    
class FactorGraphNode(Node):
    
    def __init__(self, name=None):
        super(FactorGraphNode, self).__init__(name)
        self._mailbox = Mailbox()
        
    def send_message(self, message, other_node):
        other_node._recieve_message(message)
            
    def send_all_BEC_messages(self):
        for node in self.connections:
            #print str(self) + '|' + str(self.generate_BEC_message_for(node)) + '|' + str(node)
            self.send_message(self.generate_BEC_message_for(node), node)
            
    def send_all_BSC_messages(self):
        for node in self.connections:
            self.send_message(self.generate_BSC_message_for(node), node)
            
    def send_all_noisy_BEC_messages(self, p):
        for node in self.connections:
            self.send_message(self.generate_noisy_BEC_message_for(node, p), node)
            
    def generate_noisy_BEC_message_for(self, node, p):
        if random() < p:
            return BinaryMessage(0, self)
        else:
            return self.generate_BEC_message_for(node)
            
    def generate_BEC_message_for(self, node):
        # Implemented by descendant classes
        pass
             
    def _recieve_message(self, message):
        self._mailbox.recieve_message(message)
        
    def clear_messages(self):
        self._mailbox.clear()

class VariableNode(FactorGraphNode):
    
    def __init__(self, name=None):
        super(VariableNode, self).__init__(name)
        
    def generate_BEC_message_for(self, fnode):
        if self._recieved_value != 0:
            return BinaryMessage(self._recieved_value, self)
        for data in self._mailbox.all_data_except_from(fnode):
            if data != 0:
                self._suspected_value = data
                return BinaryMessage(data, self)
        return BinaryMessage(0, self)
    
    def generate_BSC_message_for(self, fnode):
        data = [datum for datum in self._mailbox.all_data_except_from(fnode)]
        if all_agree(data) and len(data) != 0:
            return BinaryMessage(data[0], self)
        else:
            return BinaryMessage(self.recieved_value, self)
    
    def process_messages_BEC(self):
        for data in self._mailbox.all_data():
            if data != 0:
                self._suspected_value = data
                break
    def process_messages_BSC(self):
        data = [bit for bit in self._mailbox.all_data()]
        if all_agree(data):
            self._suspected_value = data[0]
        else:
            self._suspected_value = self._recieved_value
    
    def _set_recieved_value(self, recieved_value):
        self._recieved_value = recieved_value
        self._suspected_value = self._recieved_value
    
    def __set_recieved_value(self, recieved_value):
        self._set_recieved_value(recieved_value)
        
    def _get_recieved_value(self):
        return self._recieved_value
    
    def __get_recieved_value(self):
        return self._get_recieved_value()
    
    recieved_value = property(__get_recieved_value, __set_recieved_value)
    
    @property
    def suspected_value(self):
        return self._suspected_value
        
class FactorNode(FactorGraphNode):
    
    def __init__(self, name=None):
        super(FactorNode, self).__init__(name)
        
    def generate_BEC_message_for(self, vnode):
        b = 1
        for data in self._mailbox.all_data_except_from(vnode):
            b *= data
        return BinaryMessage(b, self)
    
    def generate_BSC_message_for(self, vnode):
        b = 1
        for data in self._mailbox.all_data_except_from(vnode):
            b *= data
        return BinaryMessage(b, self)
    
def all_agree(data):
    if len(data) == 1:
        return True
    elif len(data) == 0:
        return False
    else:
        datum = data[0]
        for d in data[1:]:
            if d != datum:
                return False
        return True


