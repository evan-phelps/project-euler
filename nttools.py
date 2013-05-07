#!/usr/bin/python
# -*- coding: utf-8 -*-
import gmpy
import random
import fractions
from itertools import takewhile

def primes(pstart=1, N=None):
    prime = gmpy.mpz(pstart)
    breakcondition = lambda x: True
    if N is not None:
        breakcondition = lambda x: x < N
    count = 0
    while breakcondition(count):
        prime = prime.next_prime()
        if prime.is_prime():
            count += 1
            yield prime


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.

    D = {}

    # The running integer that's checked for primeness

    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def sieveErat(N=10):

    # should probably be implemented as map to allow for quick removal
    # of eliminated numbers rather than redundantly setting the
    # booleans to False

    def getnext(i, nums):
        mx = len(nums)
        if i >= mx:
            return -1
        while i < mx and not nums[i][1] or i == 0:
            i += 1
        return i

    nums = [list(t) for t in zip(range(2, N + 1), (N - 1) * [True])]
    mx = len(nums)
    i = 0
    while i >= 0 and i < mx:
        v = nums[i][0]
        for j in range(i + v, N - 1, v):
            nums[j][1] = False
        i = getnext(i + 1, nums)
    return [n[0] for n in nums if n[1]]


def factor(N):
    """get all factors of the number N"""

    factors = []
    for x in range(2, int(math.sqrt(N))):
        (d, r) = divmod(N, x)
        if r == 0:
            factors.append(x)
            factors.append(d)

    return [1, N] + factors


def pfactorGen(N):
    """generate prime factors of the number N"""

    n = N
    p = list(takewhile(lambda x: x < N, primes(N=N)))  # gen_primes()))
    i = 0

    # divide out the lowest numbers first so that as long as the
    # reduced n is composite, it must be greater than the square of the
    # next largest number (n>i^2).

    while p[i] * p[i] <= n:
        while n % p[i] == 0:
            yield p[i]  # n is divisible by i
            n /= p[i]
        i += 1

    # the final reduced n is the last and largest non-composite (prime)
    # factor of N.

    if n > 1:
        yield int(n)


def prb(N):
    if N % 2 == 0:
        return 2
    (y, c, m) = (random.randint(1, N - 1), random.randint(1, N - 1),
                 random.randint(1, N - 1))
    (g, r, q) = (1, 1, 1)
    while g == 1:
        x = y
        for i in range(r):
            y = (y * y % N + c) % N
        k = 0
        while k < r and g == 1:
            ys = y
            for i in range(min(m, r - k)):
                y = (y * y % N + c) % N
                q = q * abs(x - y) % N
            g = fractions.gcd(q, N)
            k = k + m
        r = r * 2
    if g == N:
        while True:
            ys = (ys * ys % N + c) % N
            g = fractions.gcd(abs(x - ys), N)
            if g > 1:
                break
    return g


def pfactor(N, myprimes=None):
    if myprimes is None:
        myprimes = []
    p = gmpy.mpz(N)
    if p.is_prime():
        myprimes.append(N)
    else:
        f = prb(N)
        myprimes.append(f)
        p = pfactor(int(N / f), myprimes)
    return myprimes
