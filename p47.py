from nttools import prb

smallprimeset = set(primesbelow(100000))
smallprimes = (2,) + tuple(n for n in xrange(3, 1000, 2) if n in smallprimeset)


def primesbelow(N):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    #""" Input N>=6, Returns a list of primes, 2 <= p < N """
    correction = N % 6 > 1
    N = {0: N, 1: N - 1, 2: N + 4, 3: N + 3, 4: N + 2, 5: N + 1}[N % 6]
    sieve = [True] * (N // 3)
    sieve[0] = False
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k * k // 3::2 * k] = [False] * (
                (N // 6 - (k * k) // 6 - 1) // k + 1)
            sieve[(k * k + 4 * k - 2 * k * (i % 2)) // 3::2 * k] = [False] * (
                (N // 6 - (k * k + 4 * k - 2 * k * (i % 2)) // 6 - 1) // k + 1)
    return [2, 3] + [(3 * i + 1) | 1 for i in range(1, N // 3 - correction) if sieve[i]]


def isprime(n, precision=7):
    # http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time
    if n == 1 or n % 2 == 0:
        return False
    elif n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n < _smallprimeset:
        return n in smallprimeset


    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for repeat in range(precision):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1: continue

        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == 1: return False
            if x == n - 1: break
        else: return False

    return True


def primefactors(n, sort=False):
    factors = []

    limit = int(n ** .5) + 1
    for checker in smallprimes:
        print smallprimes[-1]
        if checker > limit:
            break
        while n % checker == 0:
            factors.append(checker)
            n //= checker

    if n < 2:
        return factors
    else:
        factors.extend(bigfactors(n, sort))
        return factors


def bigfactors(n, sort=False):
    factors = []
    while n > 1:
        if isprime(n):
            factors.append(n)
            break
        factor = prb(n)
        # recurse to factor the not necessarily prime factor returned by
        # pollard-brent
        factors.extend(bigfactors(factor, sort))
        n //= factor

    if sort:
        factors.sort()
    return factors
