from CodeMaker import make_H_gallager
from CodeMaker import LinkArrayToMatrix
from numpy import array
import numpy as np
from random import randint

def get_H(N, dv, dc):
    return array(LinkArrayToMatrix(N, make_H_gallager(N, dv, dc)))

def get_codewords(H, num_codewords):
    N = H.shape[1]
    k = H.shape[0]
    codewords = set()
    while len(codewords) < num_codewords:
        word = np.zeros((N,1))
        zero = np.zeros((k,1))
        for i in xrange(len(word)):
            word[i] = randint(0,1)
        #print word
        result = H.dot(word)
        for i in xrange(len(result)):
            result[i] %= 2
        if np.array_equal(result, zero):
            codewords.add(tuple(map(int, word.transpose()[0])))
    return codewords
            
if __name__ == '__main__':
    print get_H(12, 3, 4)
    