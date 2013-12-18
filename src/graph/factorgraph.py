'''
Created on Nov 6, 2013

@author: Erik
'''
from numpy import array
from numpy import mean
from numpy import arange
from node import VariableNode
from node import FactorNode
from random import random
import matplotlib.pyplot as plt

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
    
    def decodeBSC(self, codeword):
        self._apply_codeword(codeword)
        
        for vnode in self._variablenodes:
            vnode.send_all_BSC_messages()
        for _ in xrange(50):
            for fnode in self._factornodes:
                fnode.send_all_BSC_messages()
                fnode.clear_messages()
                
            for vnode in self._variablenodes:
                vnode.process_messages_BSC()
                vnode.send_all_BSC_messages()
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


def mainBSC():
    a = mat3()
    code = mat3allcodes()[2]
    f = FactorGraph(a)
    print code
    codeword = simulateBSC1bit(0.2, convert01(code))
    print convertneg11(codeword)
    result = f.decodeBSC(codeword)
    print convertneg11(result)
    if code == convertneg11(result):
        print 'SUCCESS'
    else:
        print 'FAIL'

def main():       
    a = mat3()
    code = mat3allcodes()[1]
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
'''
def mat1():
    return array([map(int, '100011100001111'),map(int, '010010011010111'),map(int, '001001010111011'), map(int, '000100101111101')])

def mat1code1():
    return map(int, '000000000000000')
'''
def simulateBSC1bit(p, codeword):
    bitflipped = False
    transmitted = []
    for bit in codeword:
        if random() < p and not bitflipped:
            print 'BITFLIPPED'
            transmitted.append(bit * -1)
            bitflipped = True
        else:
            transmitted.append(bit)
    return transmitted
    
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

def mat3():
    return array([map(int, '111100'), map(int, '001101'), map(int, '100110')])

def mat3allcodes():
    return [map(int, '000000'), map(int, '011001'), map(int, '110010'), map(int, '101011'), map(int, '111100'), map(int, '100101'), map(int, '001110')]

def all2errors(codeword):
    lst = []
    for i in xrange(len(codeword)-2):
        for j in xrange(i+1, len(codeword) - 1):
            current = list(codeword)
            current[i] = 0
            current[j] = 0
            lst.append(current)
    return lst

def testsuite():
    #f = FactorGraph(mat3())
    all_codes = mat3allcodes()
    
    #code = convert01([0,0,1,1,1,0])
    #error = [0,1,-1,0,-1,1]
    #result = f.decodeBEC(error)
    
    #print convertneg11(code)
    #print convertneg11(error)
    #print convertneg11(result)
    P = arange(0, 0.75, 0.05)
    avg = {}
    all_success = True
    LOGFILE = 'data.txt'
    datafile = open(LOGFILE, 'wb')
    for p in P:
        datafile.write('******* p = ' + str(p) + '*******\n')
        for code in all_codes:
            num_iter = []
            datafile.write('**' + str(code) + '**\n')
            code = convert01(code)
            errors = all2errors(code)
            for error in errors:
                datafile.write(str(convertneg11(error)) + '\n'),
                f = FactorGraph(mat3())
                r = f.decodeBEC(error, p, 50000)
                result = r[0]
                num_iter.append(r[1])
                if result == code:
                    datafile.write('SUCCESS ' + str(r[1]) + '\n')
                else:
                    datafile.write('FAIL' + str(convertneg11(result)) + '\n')
                    all_success = False
        avg[p] = mean(num_iter)
    if all_success:
        datafile.write('ALL SUCCESSFUL\n')
    else:
        datafile.write('FAILURE OCCURRED\n')
    for point in avg:
        plt.plot(point, avg[point], 'ro')
    plt.xlabel('Probability of message-passing failure')
    plt.ylabel('Number of iterations')
    plt.title('Average number of iterations until convergence')
    plt.show()
    
    datafile.close()
    
if __name__ == '__main__':
    mainBSC()            
