'''
Created on Nov 6, 2013

@author: Erik
'''

from node import VariableNode
from node import FactorNode

class FactorGraph(object):
    
    def __init__(self, check_array):
        self._factornodes = []
        self._variablenodes = []
        n = check_array.shape[0]
        m = check_array.shape[1]
        for i in xrange(m):
            self._variablenodes.append(VariableNode('v' + str(i)))
        for i in xrange(n):
            fnode = FactorNode('f' + str(i))
            self._factornodes.append(fnode)
            check_array_row = check_array[i, :]
            for j, a in enumerate(check_array_row):
                if a:
                    vnode = self._variablenodes[j]
                    fnode.add_undirected_connection(vnode)
                     
    def decodeBEC(self, codeword, p=0, max_iter=500):
        self._apply_codeword(codeword)
        
        for vnode in self._variablenodes:
            vnode.send_all_noisy_BEC_messages(p)
        num_iter = 0
        while 0 in self._get_suspected_result() and num_iter < max_iter:
            num_iter += 1
            for fnode in self._factornodes:
                fnode.send_all_noisy_BEC_messages(p)
                fnode.clear_messages()
                
            for vnode in self._variablenodes:
                vnode.process_messages_BEC()
                vnode.send_all_noisy_BEC_messages(p)
                vnode.clear_messages()    
        return (self._get_suspected_result(), num_iter)
    
    def decode_BEC_memoryless(self, codeword, p=0, max_iter=500):
        self._apply_codeword(codeword)
        
        for _ in xrange(max_iter):
            for vnode in self._variablenodes:
                vnode.send_all_noisy_BEC_messages(p)
                vnode.clear_messages()
            for fnode in self._factornodes:
                fnode.send_all_noisy_BEC_messages(p)
                fnode.clear_messages()
        for vnode in self._variablenodes:
            vnode.process_messages_BEC()
        return self._get_suspected_result()
    
    def decode_BEC_memory(self, codeword, p=0, max_iter=500):
        self._apply_codeword(codeword)
        
        for _ in xrange(max_iter):
            for vnode in self._variablenodes:
                vnode.send_all_noisy_BEC_messages(p)
                vnode.process_messages_BEC()
                vnode.clear_messages()
            for fnode in self._factornodes:
                fnode.send_all_noisy_BEC_messages(p)
                fnode.clear_messages()
        for vnode in self._variablenodes:
            vnode.process_messages_BEC()
        return self._get_suspected_result()
    
    def decodeBSC(self, codeword, p=0):
        self._apply_codeword(codeword)
        
        for vnode in self._variablenodes:
            vnode.send_all_noisy_BSC_messages(p)
        for _ in xrange(50):
            for fnode in self._factornodes:
                fnode.send_all_noisy_BSC_messages(p)
                fnode.clear_messages()
                
            for vnode in self._variablenodes:
                vnode.process_messages_BSC()
                vnode.send_all_noisy_BSC_messages(p)
                vnode.clear_messages()
        return self._get_suspected_result()
        
    def _apply_codeword(self, codeword):
        for i, vnode in enumerate(self._variablenodes):
            vnode.recieved_value = codeword[i]
            
    def _get_suspected_result(self):
        result = []
        for vnode in self._variablenodes:
            result.append(vnode.suspected_value)
        return result
            
    def __repr__(self):
        return '<' + str(self._factornodes) + '>'
    
    def __str__(self):
        s = '<Factor Graph ' + str(id(self)) + '\n'
        for fnode in self._factornodes:
            s += '    ' + str(fnode) + '\n'
        s += '>'
        return s            
