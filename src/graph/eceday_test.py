'''
Created on May 2, 2014

@author: erik
'''

from communication.ldpc_codes import get_H
from communication.ldpc_codes import get_codewords
from factorgraph import FactorGraph
from random import random
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def main():
    test_N()
    
def test_N():
    use_sql = False
    if(use_sql):
        conn = sqlite3.connect('blocklength.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE points
                 (N integer, alpha real, beta real, perror real, sd real)''')
    dv = 3
    dc = 6
    alpha = 0.25
    beta = 0.1
    START = 450
    END = 450
    STEP = START
    REPEAT = 10
    TRIALS = 15
    for N in xrange(START, END + STEP, STEP):
        if(use_sql):
            conn.commit()
        print '***', N, '***'
        H = get_H(N, dv, dc)
        # print 'H DONE'
        word = [0] * N
        max_iter = N / 4
        failure_rate = [0] * TRIALS
        noiseless_failure_rate = [0] * TRIALS
        for i in xrange(TRIALS):
            for _ in xrange(REPEAT):
                # print i
                codeword = word
                codeword = convert_to_posneg(codeword)
                codeword = simulateBEC(alpha, codeword)
                f = FactorGraph(H)
                codeword = f.decode_BEC_memory(codeword, beta, max_iter)
                codeword = convert_to_zeroone(codeword)
                if codeword != word:
                    failure_rate[i] += 1.0 / REPEAT
        # print 'SD', np.std(failure_rate)
        if N == START:
            plt.errorbar(N, np.average(failure_rate), np.std(failure_rate), linestyle='None', marker='o', color='red', label='beta = 0.1')
        else:
            plt.errorbar(N, np.average(failure_rate), np.std(failure_rate), linestyle='None', marker='o', color='red')
        if(use_sql):
            c.execute('INSERT INTO points VALUES (?,?,?,?,?)', (N, alpha, beta, np.average(failure_rate), np.std(failure_rate)))
        '''
        for i in xrange(TRIALS):
            for _ in xrange(REPEAT):
                # print i
                codeword = word
                codeword = convert_to_posneg(codeword)
                codeword = simulateBEC(alpha, codeword)
                f = FactorGraph(H)
                codeword = f.decode_BEC_memoryless(codeword, 0, max_iter)
                codeword = convert_to_zeroone(codeword)
                if codeword != word:
                    noiseless_failure_rate[i] += 1.0 / REPEAT
        if N == START:
            plt.errorbar(N, np.average(noiseless_failure_rate), np.std(noiseless_failure_rate), linestyle='None', marker='o', color='blue', label='beta = 0')
        else:
            plt.errorbar(N, np.average(noiseless_failure_rate), np.std(noiseless_failure_rate), linestyle='None', marker='o', color='blue')
        if(use_sql):
            c.execute('INSERT INTO points VALUES (?,?,?,?,?)', (N, alpha, 0, np.average(noiseless_failure_rate), np.std(noiseless_failure_rate)))
        #plt.show()
        '''
    #for point in noisy_results:
    #    plt.plot(point[0], point[1], 'ro')
    #for point in noiseless_results:
    #    plt.plot(point[0], point[1], 'bo')
    plt.axis((0, N + STEP, -0.05, 0.5))
    plt.xlabel('Block Length')
    plt.ylabel('Probability of Error')
    plt.legend(loc='upper right')
    plt.suptitle('Block Length vs. Probability of Error for alpha = 0.25')
    plt.xticks(np.arange(0, END + STEP, STEP))
    plt.yticks(np.arange(0, 0.5 + 0.05, 0.05))
    if(use_sql):
        conn.commit()
    print 'DONE'
    plt.show()

def test_beta():
    N = 30
    dv = 3
    dc = 6
    num_codewords = 10
    H = get_H(N,dv,dc)
    codewords = get_codewords(H, num_codewords)
    p = 0.25
    max_iter = 10
    trials = 100
    print 'GOT ALL CODEWORDS'
    step = 0.1
    b = np.arange(0, 0.5, step)
    results = set()
    for beta in b:
        success_rate = [0] * num_codewords
        print beta,
        for i, word in enumerate(codewords):
            for _ in xrange(trials):
                codeword = word
                codeword = convert_to_posneg(codeword)
                codeword = simulateBEC(p, codeword)
                f = FactorGraph(H)
                codeword = f.decode_BEC_memoryless(codeword, beta, max_iter)
                codeword = convert_to_zeroone(codeword)
                if tuple(codeword) == word:
                    success_rate[i] += 1 / float(trials)
        stat = np.average(success_rate)
        print stat
        results.add(tuple([beta, stat]))
    print results
    for point in results:
        plt.plot(point[0], point[1], 'ro')
    plt.show()
    
def convert_to_posneg(codeword):
    newcodeword = []
    for bit in codeword:
        if bit == 0:
            newcodeword.append(1)
        elif bit == 1:
            newcodeword.append(-1)
    return newcodeword

def convert_to_zeroone(codeword):
    newcodeword = []
    for bit in codeword:
        if bit == 1:
            newcodeword.append(0)
        elif bit == -1:
            newcodeword.append(1)
        elif bit == 0:
            newcodeword.append('e')
    return newcodeword

def simulateBEC(p, codeword):
    transmitted = []
    for bit in codeword:
        if random() < p:
            transmitted.append(0)
        else:
            transmitted.append(bit)
    return transmitted

if __name__ == '__main__':
    main()