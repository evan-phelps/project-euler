from sympy import ntheory as nt
# TODO: performance tweak
#           1. determine maximum possible series length (1st iter starts with 2)
#           2. subtract from top until prime sum or until series length is less
#               than previous streak... (streak, sum)
#           3. subtract lowest prime in streak
#           4. repeat 1-3 until max series length < streak


def sumcons(Nmin, Nmax):
    retval = (-1, -1)
    tot = 0
    for i, n in enumerate(nt.primerange(Nmin, Nmax)):
        if i == 0:
            continue
        if tot >= Nmax:
            break
        if nt.isprime(tot):
            retval = (i, tot)
        tot = tot + n
    return retval

Nmax = 1000000
start = 1
nconsprimes = []
tots = []
while start < Nmax:
    (n, N) = sumcons(start, Nmax)
    if n > 0:
        nconsprimes.append(n)
        tots.append(N)
    start = nt.nextprime(start)

print(max([(n, N) for (n, N) in zip(nconsprimes, tots) if n > 20]))
