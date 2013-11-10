'''
Created on Nov 6, 2013

@author: Erik
'''
class CommunicationException(Exception):
    pass

class MessageError(CommunicationException):
    pass

class BinaryMessageError(MessageError):
    pass
