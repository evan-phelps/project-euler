# !!! assumes python3 !!! ... but python2 might work
# I noticed that python2 seems to execute some of these algorithms more
# quickly than python3!

import datetime
from itertools import takewhile
from itertools import repeat
from itertools import tee
import operator as op
from functools import reduce
try: import numpypy # for pypy experimental support
except ImportError: pass
import numpy

# in case of command-line timeit, set stdoutON = False, i.e., from bash
# python -mtimeit -s "import solutions as pe"\
#                    "pe.stdoutON=False" "pe.p1(100000)"\
#                     | awk -F' ' '{print $6, $7}';
stdoutON = True

# #####################################################################
# ######################### UTILITY FUNCTIONS #########################
# #####################################################################

def timeit(method):
    """timing decorator"""
    def timed(*args, **kw):
        if stdoutON:
            ts = datetime.datetime.now()
            result = method(*args, **kw)
            te = datetime.datetime.now()
            t = te-ts
            print('setup and execution time: %s (H:mm:ss.uuuuuu)'%str(t))
            return result
        else: return method(*args, **kw)
    return timed

def part(l, N):
    """partition list 'l' into sublists of length 'N'"""
    return [l[n:n+N] for n in range(0,len(l),N)]

def pfactorGen(N):
    """generate prime factors of the number N"""
    i = 2
    n = N
    # divide out the lowest numbers first so that as long as the
    # reduced n is composite, it must be greater than the square of the
    # next largest number (n>i^2).
    while i*i < n:
        while n%i == 0:
            yield i      # n is divisible by i
            n /= i
        i += 1
    # the final reduced n is the last and largest non-composite (prime)
    # factor of N.
    yield int(n)

# #####################################################################
# ######################## SOLUTION FUNCTIONS #########################
# #####################################################################

# comment @timeit decorator if running command-line timeit function to
# avoid superfluous print statement during loop

@timeit
def p1(lt=1000):
    """P1: 'Find the sum of all the multiples of 3 or 5 below 1000.'"""
    def mod35Gen():
        # see p1_ana; use 7-number cycle in n(i+1)-n(i) of mult-3,5
        # number sequence to generate series
        toadd = [3, 2, 1, 3, 1, 2, 3]
        a = 0
        i = 0
        while 1:
            a += toadd[i]
            yield a
            if i >= 6: i = 0
            else: i+=1

    g = mod35Gen()
    # sum elements of mod3||mod5 series up to value 'lt'
    return reduce(op.add, takewhile(lambda x: x < lt, g))

@timeit
def p2(lt=4000000, fltr=lambda x:x%2==0):
    """P2: By considering the terms in the Fibonacci sequence whose
    values do not exceed four million, find the sum of the even-valued
    terms.
    """
    def fibGen():
        # fibonacci generator; since we need to sum all elements, no
        # need to use optimized expression to extract element N
        a,b=0,1
        while True:
            yield a
            a,b = b,a+b
    fg = fibGen()
    # filter and sum even elements of fibonacci series up to value 'lt'
    return reduce(op.add, filter(fltr,takewhile(lambda x: x < lt, fg)))

@timeit
def p3(N=600851475143):
    """P3: What is the largest prime factor of the number 600851475143?
    """
    # first attempt was to your a prime sieve first and then filter
    # the factors, but my naive prime sieve (Eratosthenes)
    # implementation ran into performance issues.  Maybe worth trying
    # a more sophisticated sieve, or an implementation language that
    # supports tail recursion (?).
    return max(pfactorGen(N))

@timeit
def p4():
    """Find the largest palindrome made from the product of two 3-digit
    numbers.
    """
    l1,l2 = range(999,99,-1),range(999,99,-1)
    # not as fast as explicit sort and for-loop in p4b, but if you like
    # so-called "pythonic" list comprehension define list of palindrome
    # products, making sure to skip duplicate multiplicand-multiplier
    # combinations
    p = [i*j for i in l1 for j in l2 
         if i<=j and (lambda x: x==x[::-1])(str(i*j))]
    return(max(p))

@timeit
def p4b():
    """Find the largest palindrome made from the product of two 3-digit
    numbers.
    """
    # faster to sort, then test for palindrome from highest to lowest
    l1,l2 = range(999,99,-1),range(999,99,-1)
    p = [i*j for i in l1 for j in l2 if i<=j]
    p.sort()
    for i in range(-1,-1*len(p),-1):
        s = str(p[i])
        if s == s[::-1]:
            return s
    return('no palindrome found')

@timeit
def p4numpy():
    """Find the largest palindrome made from the product of two 3-digit
    numbers.
    """
    # faster with numpy in python
    # pypy numpy experimental (sort broken as of 4/26/2013)
    # pypy p4 and p4b slightly faster than numpy in python
    a = numpy.arange(100,1000)
    ns = numpy.outer(a,a)
    ns = numpy.ravel(ns)
    ns.sort()
    for i in range(-1,-1*len(ns),-1):
        s = str(ns[i])
        if s == s[::-1]:
            print(s)
            break

# #####################################################################
# ################# PRELIMINARY ANALYSIS FUNCTIONS ####################
# #####################################################################

def p1_ana():
    # some observations about series of mult-3,5 numbers
    l1 = [i for i in range(0,374) if i%3==0 or i%5==0]
    l2 = [i for i in range(3,377) if i%3==0 or i%5==0]
    toadd = [x2-x1 for x1,x2 in zip(l1,l2)]
    toadd2 = part(toadd,7)
    msg = 'Notice the pattern of n(i+1)-n(i):'
    msglen = len(msg)
    print(msg+'\n'+''.join(repeat('=',msglen)))
    seqstrlen = len(str(toadd2[0]))
    for n7 in toadd2:
        print(str("%%+%ds"%(msglen-(msglen-seqstrlen+2)/2)) % str(n7))
