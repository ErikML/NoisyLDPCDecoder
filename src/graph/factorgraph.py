'''
Created on Nov 6, 2013

@author: Erik
'''
from numpy import array
from node import VariableNode
from node import FactorNode
from random import random

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
                     
    def decodeBEC(self, codeword):
        self._apply_codeword(codeword)
        
        for vnode in self._variablenodes:
            vnode.send_all_BEC_messages()
        
        p = 0.99
        for _ in xrange(50000):
            for fnode in self._factornodes:
                fnode.send_all_noisy_BEC_messages(p)
                fnode.clear_messages()
                
            for vnode in self._variablenodes:
                vnode.process_messages_BEC()
                vnode.send_all_noisy_BEC_messages(p)
                vnode.clear_messages()    
        result = []
        for vnode in self._variablenodes:
            result.append(vnode.suspected_value) 
        return result
        
    def _apply_codeword(self, codeword):
        for i, vnode in enumerate(self._variablenodes):
            vnode.recieved_value = codeword[i]
            
    def __repr__(self):
        return '<' + str(self._factornodes) + '>'
    
    def __str__(self):
        s = '<Factor Graph ' + str(id(self)) + '\n'
        for fnode in self._factornodes:
            s += '    ' + str(fnode) + '\n'
        s += '>'
        return s


def main():       
    a = mat2()
    code = mat2code2()
    f = FactorGraph(a)
    print code
    codeword = simulateBEC(0.4, convert01(code))
    print convertneg11(codeword)
    result = f.decodeBEC(codeword)
    print convertneg11(result)
    if code == convertneg11(result):
        print 'SUCCESS'
    else:
        print 'FAIL'

def mat1():
    return array([map(int, '100011100001111'),map(int, '010010011010111'),map(int, '001001010111011'), map(int, '000100101111101')])

def mat1code1():
    return map(int, '000000000000000')

def mat2():
    return array([map(int, '10100'), map(int, '11010'), map(int, '01001')])

def mat2code1():
    return map(int, '10110')

def mat2code2():
    return map(int, '11101')

def mat2code3():
    return map(int, '00000')

def convert01(codeword):
    newcodeword = []
    for bit in codeword:
        if bit == 0:
            newcodeword.append(1)
        elif bit == 1:
            newcodeword.append(-1)
    return newcodeword

def simulateBEC(p, codeword):
    transmitted = []
    for bit in codeword:
        if random() < p:
            transmitted.append(0)
        else:
            transmitted.append(bit)
    return transmitted

def convertneg11(codeword):
    newcodeword = []
    for bit in codeword:
        if bit == 1:
            newcodeword.append(0)
        elif bit == -1:
            newcodeword.append(1)
        elif bit == 0:
            newcodeword.append('?')
    return newcodeword
    
if __name__ == '__main__':
    main()            
