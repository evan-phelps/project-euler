# !!! assumes python3 !!! ... but python2 might work
# I noticed that python2 seems to execute some of these algorithms more
# quickly than python3!

import datetime
import math
from itertools import takewhile
from itertools import repeat
from itertools import tee
import operator as op
from functools import reduce
from collections import Counter
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
    while i*i <= n:
        while n%i == 0:
            yield i      # n is divisible by i
            n /= i
        i += 1
    # the final reduced n is the last and largest non-composite (prime)
    # factor of N.
    yield int(n)

def sieveErat(N=10):
    # should probably be implemented as map to allow for quick removal
    # of eliminated numbers rather than redundantly setting the
    # booleans to False
    def getnext(i,nums):
        mx = len(nums)
        if i >= mx: return -1
        while i < mx and not nums[i][1] or i == 0: i += 1
        return i
    nums = [list(t) for t in zip(range(2,N+1),(N-1)*[True])]
    mx = len(nums)
    i = 0
    while i >= 0 and i < mx:
        v = nums[i][0]
        for j in range(i+v,N-1,v): nums[j][1] = False
        i = getnext(i+1,nums)
    return [n[0] for n in nums if n[1]]

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

@timeit
def p5(N=20):
    """What is the smallest positive number that is evenly divisible
    by all of the numbers from 1 to 20?
    """
    # Factors of smallest number evenly divisible by every number
    # from 1 to N given as follows:  from all numbers between 2 and
    # N, take the maximum multiplicity (n_i) of each factor (i).
    fcounters = [Counter(pfactorGen(n)) for n in range(2,N+1)]
    factors = Counter()
    for fc in fcounters:
        for k,v in fc.items():
            if v>factors[k]: factors[k]=v
    answer = 1
    for k,v in factors.items(): answer *= k**v  #print(k,v)
    return answer
    
@timeit
def p6(N=100):
    """Find the difference between the sum of the squares of the first
    one hundred natural numbers and the square of the sum.
    """
    return sum(2*i*j for i,j in combinations(range(1,N+1),2))

@timeit
def p7(nth=10001):
    """What is the 10001st prime number?"""
    # currently, from command line, need to get 100001st element from
    # returned list. need to implement generator for this instead!
    # for now, I'll estimate how many to pull based on the prime
    # number theorem.
    N = nth
    while nth > N/(math.log(N)-1): N *= 1.1
    N = int(N)
    print('estimated N = %d' % N)
    return list(sieveErat(int(N)))[nth-1]

@timeit
def p8():
    """Find the greatest product of five consecutive digits in the
    1000-digit number.
    """
    nstr = '7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'
    l = len(nstr)
    mx = 0
    for i in range(0,l-5):
        prod = reduce(op.mul,[int(d) for d in nstr[i:i+5]])
        if mx < prod: mx = prod
    return mx

@timeit
def p9():
    """There exists exactly one Pythagorean triplet for which
    a + b + c = 1000.  Find the product abc.
    """
    for b in range(1,1000):
        for a in range(1,b):
            c = pow(a**2+b**2,0.5)
            if a+b+c==1000:
                return a*b*c
@timeit
def p10(N=10):
    """Find the sum of all the primes below two million."""
    return sum(sieveErat(N))
    
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
