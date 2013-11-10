'''
Created on Nov 6, 2013

@author: Erik
'''
from exception_communication import BinaryMessageError

class Message(object):
    
    def __init__(self, data, sender):
        self._data = data
        self._sender = sender
        
    def __repr__(self):
        return 'Message('+str(self.data)+','+str(self.sender)+')'
        
    @property
    def data(self):
        return self._data
    
    @property
    def sender(self):
        return self._sender

class BinaryMessage(Message):
    
    def __init__(self, data, sender):
        allowed_data = [-1, 0, 1]
        if data not in allowed_data:
            raise BinaryMessageError(data + ' is not binary data')
        else:
            super(BinaryMessage, self).__init__(data, sender)
            
class Mailbox(object):
        
        def __init__(self):
            self._mailbox = set()
            
        def recieve_message(self, message):
            self._mailbox.add(message)
            
        def all_data(self):
            data = set()
            for message in self._mailbox:
                data.add(message.data)
            return data
            
        def all_data_except_from(self, sender):
            data = []
            for message in self._mailbox:
                if message.sender is sender:
                    continue
                else:
                    data.append(message.data)
            return data
        
        def clear(self):
            self._mailbox = set()     
            