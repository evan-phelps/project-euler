MAX      = 1000000
is_prime = [True]*MAX

for i in range(2,MAX): 
    if is_prime[i]:
        for j in range(2*i,MAX,i):
            is_prime[j] = False

primes = [ p for p in range(2,MAX) if is_prime[p]]

curSum = sum(primes)
N = L  = len(primes)

# Find maximum starting length (N) 
# cut off the last/tail primes  if it exceed MAX 

while curSum >= MAX:
    N      -= 1
    curSum -= primes[N]

while N  > 0:
    N -= 1
    # Sum of first N primes
    curSum    = sum(primes[:N]) 
    head,tail = 0,N

    # Do not recalculate consecutive sum, add tail and substract head
    while curSum < MAX and not is_prime[curSum] and tail < L:
        curSum -= primes[head]
        curSum += primes[tail]
        head   += 1
        tail   += 1

    if curSum < MAX and is_prime[curSum] :
        print curSum
        break