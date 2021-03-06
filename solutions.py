# !!! assumes python3 !!! ... but python2 might work
# I noticed that python2 seems to execute some of these algorithms more
# quickly than python3!

import datetime
import math
import operator as op
from functools import reduce
from collections import Counter
import datetime as dt
import sympy as sp

from itertools import takewhile, repeat, combinations, permutations, islice
import numpy
import gmpy

import nttools

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
            print('setup and execution time: %s (H:mm:ss.uuuuuu)' % str(t))
            return result
        else:
            return method(*args, **kw)
    return timed


def part(l, N):
    """partition list 'l' into sublists of length 'N'"""
    return [l[n:n+N] for n in range(0, len(l), N)]

# #####################################################################
# ######################## SOLUTION FUNCTIONS #########################
# #####################################################################


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
            i = 0 if i >= 6 else i+1

    g = mod35Gen()
    # sum elements of mod3||mod5 series up to value 'lt'
    return reduce(op.add, takewhile(lambda x: x < lt, g))


@timeit
def p2(lt=4000000, fltr=lambda x: x % 2 == 0):
    """P2: By considering the terms in the Fibonacci sequence whose
    values do not exceed four million, find the sum of the even-valued
    terms.
    """
    fg = nttools.gen_fib()
    # filter and sum even elements of fibonacci series up to value 'lt'
    return reduce(op.add, filter(fltr, takewhile(lambda x: x < lt, fg)))


@timeit
def p3(N=600851475143):
    """P3: What is the largest prime factor of the number 600851475143?
    """
    # First attempt was to use a prime sieve first and then filter
    # the factors, but my naive prime sieve (Eratosthenes)
    # implementation ran into performance issues. This version uses
    # the Pollard-Rho-Brent algorithm -- very, very efficient.
    return max(nttools.pfactor(N))


@timeit
def p4():
    """Find the largest palindrome made from the product of two 3-digit
    numbers.
    """
    l1, l2 = range(999, 99, -1), range(999, 99, -1)
    # not as fast as explicit sort and for-loop in p4b, but if you like
    # so-called "pythonic" list comprehension define list of palindrome
    # products, making sure to skip duplicate multiplicand-multiplier
    # combinations
    p = [i*j for i in l1 for j in l2
         if i <= j and (lambda x: x == x[::-1])(str(i*j))]
    return(max(p))


@timeit
def p4b():
    """Find the largest palindrome made from the product of two 3-digit
    numbers.
    """
    # faster to sort, then test for palindrome from highest to lowest
    l1, l2 = range(999, 99, -1), range(999, 99, -1)
    p = [i * j for i in l1 for j in l2 if i <= j]
    p.sort()
    for i in range(-1, -1 * len(p), -1):
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
    a = numpy.arange(100, 1000)
    ns = numpy.outer(a, a)
    ns = numpy.ravel(ns)
    ns.sort()
    for i in range(-1, -1 * len(ns), -1):
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
    fcounters = [Counter(nttools.pfactor(N=n)) for n in range(2, N+1)]
    #could also have used pfactorGen(n)
    factors = Counter()
    for fc in fcounters:
        for k, v in fc.items():
            factors[k] = v if v > factors[k] else factors[k]
    return reduce(op.mul, [k**v for k, v in factors.items()], 1)


@timeit
def p6(N=100):
    """Find the difference between the sum of the squares of the first
    one hundred natural numbers and the square of the sum.
    """
    return sum(2*i*j for i, j in combinations(range(1, N+1), 2))


@timeit
def p7(N=10001):
    """What is the 10001st prime number?"""
    for i, tin in enumerate(nttools.gen_primes()):
        if i >= N-1:
            return tin
            break
    #return list(takewhile(lambda x: x[0]<N, enumerate(nttools.gen_primes())))[N-1]


@timeit
def p7alt2(N=10001):
    """What is the 10001st prime number?"""
    for i, p in enumerate(nttools.primes()):
        if i >= N-1:
            return p
            break
    return -1
    #return list(nttools.primes(1, N))[N-1]


@timeit
def p7alt(nth=10001):
    """What is the 10001st prime number?"""
    N = nth
    while nth > N/(math.log(N)-1):
        N *= 1.1
    N = int(N)
    #print('estimated N = %d' % N)
    return list(nttools.sieveErat(int(N)))[nth-1]


@timeit
def p8():
    """Find the greatest product of five consecutive digits in the
    1000-digit number.
    """
    nstr = '7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450'
    l = len(nstr)
    mx = 0
    for i in range(0, l-5):
        prod = reduce(op.mul, [int(d) for d in nstr[i:i+5]])
        mx = prod if mx < prod else mx
    return mx


@timeit
def p9():
    """There exists exactly one Pythagorean triplet for which
    a + b + c = 1000.  Find the product abc.
    """
    for b in range(1, 1000):
        for a in range(1, b):
            c = pow(a**2+b**2, 0.5)
            if a+b+c == 1000:
                return a*b*c


@timeit
def p10(N=10):
    """Find the sum of all the primes below two million."""
    return sum(nttools.sieveErat(N))


@timeit
def p11():
    """What is the greatest product of four adjacent numbers in the same
    direction (up, down, left, right, or diagonally) in the 2020 grid?
    46
    """
    grid = [['08', '02', '22', '97', '38', '15', '00', '40', '00', '75', '04', '05', '07', '78', '52', '12', '50', '77', '91', '08'],
            ['49', '49', '99', '40', '17', '81', '18', '57', '60', '87', '17', '40', '98', '43', '69', '48', '04', '56', '62', '00'],
            ['81', '49', '31', '73', '55', '79', '14', '29', '93', '71', '40', '67', '53', '88', '30', '03', '49', '13', '36', '65'],
            ['52', '70', '95', '23', '04', '60', '11', '42', '69', '24', '68', '56', '01', '32', '56', '71', '37', '02', '36', '91'],
            ['22', '31', '16', '71', '51', '67', '63', '89', '41', '92', '36', '54', '22', '40', '40', '28', '66', '33', '13', '80'],
            ['24', '47', '32', '60', '99', '03', '45', '02', '44', '75', '33', '53', '78', '36', '84', '20', '35', '17', '12', '50'],
            ['32', '98', '81', '28', '64', '23', '67', '10', '26', '38', '40', '67', '59', '54', '70', '66', '18', '38', '64', '70'],
            ['67', '26', '20', '68', '02', '62', '12', '20', '95', '63', '94', '39', '63', '08', '40', '91', '66', '49', '94', '21'],
            ['24', '55', '58', '05', '66', '73', '99', '26', '97', '17', '78', '78', '96', '83', '14', '88', '34', '89', '63', '72'],
            ['21', '36', '23', '09', '75', '00', '76', '44', '20', '45', '35', '14', '00', '61', '33', '97', '34', '31', '33', '95'],
            ['78', '17', '53', '28', '22', '75', '31', '67', '15', '94', '03', '80', '04', '62', '16', '14', '09', '53', '56', '92'],
            ['16', '39', '05', '42', '96', '35', '31', '47', '55', '58', '88', '24', '00', '17', '54', '24', '36', '29', '85', '57'],
            ['86', '56', '00', '48', '35', '71', '89', '07', '05', '44', '44', '37', '44', '60', '21', '58', '51', '54', '17', '58'],
            ['19', '80', '81', '68', '05', '94', '47', '69', '28', '73', '92', '13', '86', '52', '17', '77', '04', '89', '55', '40'],
            ['04', '52', '08', '83', '97', '35', '99', '16', '07', '97', '57', '32', '16', '26', '26', '79', '33', '27', '98', '66'],
            ['88', '36', '68', '87', '57', '62', '20', '72', '03', '46', '33', '67', '46', '55', '12', '32', '63', '93', '53', '69'],
            ['04', '42', '16', '73', '38', '25', '39', '11', '24', '94', '72', '18', '08', '46', '29', '32', '40', '62', '76', '36'],
            ['20', '69', '36', '41', '72', '30', '23', '88', '34', '62', '99', '69', '82', '67', '59', '85', '74', '04', '36', '16'],
            ['20', '73', '35', '29', '78', '31', '90', '01', '74', '31', '49', '71', '48', '86', '81', '16', '23', '57', '05', '54'],
            ['01', '70', '54', '71', '83', '51', '54', '69', '16', '92', '33', '48', '61', '43', '52', '01', '89', '19', '67', '48']]
    nrows = len(grid)
    ncols = len(grid[0])
    maxprod = 0
    #ugly solution
    for i in range(0, nrows):
        for j in range(0, ncols):
            if j < ncols-4:
                val = 1
                for v in [int(grid[i][j+j1]) for j1 in range(0, 4)]:
                    val *= v
                if val > maxprod:
                    maxprod = val
            if i < nrows-4:
                val = 1
                for v in [int(grid[i+i1][j]) for i1 in range(0, 4)]:
                    val *= v
                if val > maxprod:
                    maxprod = val
            if i < nrows-4 and j < ncols-4:
                val = 1
                for v in [int(grid[i+dinc][j+dinc]) for dinc in range(0, 4)]:
                    val *= v
                if val > maxprod:
                    maxprod = val
            if i > 2 and j < ncols-4:
                val = 1
                for v in [int(grid[i-dinc][j+dinc]) for dinc in range(0, 4)]:
                    val *= v
                if val > maxprod:
                    maxprod = val
    return maxprod


@timeit
def p12(N=5, N0=1):
    """What is the value of the first triangle number to have over five
    hundred divisors?
    """
    n = N0
    nfs = 1
    for i, n in [(i, i*(i+1)/2) for i in range(N0, N+1)]:
        nfs = len(nttools.factor(n))
        if nfs >= 500:
            print(i, nfs, int(n))
            break
    return int(n)


@timeit
def p13():
    nums = [37107287533902102798797998220837590246510135740250,
            46376937677490009712648124896970078050417018260538,
            74324986199524741059474233309513058123726617309629,
            91942213363574161572522430563301811072406154908250,
            23067588207539346171171980310421047513778063246676,
            89261670696623633820136378418383684178734361726757,
            28112879812849979408065481931592621691275889832738,
            44274228917432520321923589422876796487670272189318,
            47451445736001306439091167216856844588711603153276,
            70386486105843025439939619828917593665686757934951,
            62176457141856560629502157223196586755079324193331,
            64906352462741904929101432445813822663347944758178,
            92575867718337217661963751590579239728245598838407,
            58203565325359399008402633568948830189458628227828,
            80181199384826282014278194139940567587151170094390,
            35398664372827112653829987240784473053190104293586,
            86515506006295864861532075273371959191420517255829,
            71693888707715466499115593487603532921714970056938,
            54370070576826684624621495650076471787294438377604,
            53282654108756828443191190634694037855217779295145,
            36123272525000296071075082563815656710885258350721,
            45876576172410976447339110607218265236877223636045,
            17423706905851860660448207621209813287860733969412,
            81142660418086830619328460811191061556940512689692,
            51934325451728388641918047049293215058642563049483,
            62467221648435076201727918039944693004732956340691,
            15732444386908125794514089057706229429197107928209,
            55037687525678773091862540744969844508330393682126,
            18336384825330154686196124348767681297534375946515,
            80386287592878490201521685554828717201219257766954,
            78182833757993103614740356856449095527097864797581,
            16726320100436897842553539920931837441497806860984,
            48403098129077791799088218795327364475675590848030,
            87086987551392711854517078544161852424320693150332,
            59959406895756536782107074926966537676326235447210,
            69793950679652694742597709739166693763042633987085,
            41052684708299085211399427365734116182760315001271,
            65378607361501080857009149939512557028198746004375,
            35829035317434717326932123578154982629742552737307,
            94953759765105305946966067683156574377167401875275,
            88902802571733229619176668713819931811048770190271,
            25267680276078003013678680992525463401061632866526,
            36270218540497705585629946580636237993140746255962,
            24074486908231174977792365466257246923322810917141,
            91430288197103288597806669760892938638285025333403,
            34413065578016127815921815005561868836468420090470,
            23053081172816430487623791969842487255036638784583,
            11487696932154902810424020138335124462181441773470,
            63783299490636259666498587618221225225512486764533,
            67720186971698544312419572409913959008952310058822,
            95548255300263520781532296796249481641953868218774,
            76085327132285723110424803456124867697064507995236,
            37774242535411291684276865538926205024910326572967,
            23701913275725675285653248258265463092207058596522,
            29798860272258331913126375147341994889534765745501,
            18495701454879288984856827726077713721403798879715,
            38298203783031473527721580348144513491373226651381,
            34829543829199918180278916522431027392251122869539,
            40957953066405232632538044100059654939159879593635,
            29746152185502371307642255121183693803580388584903,
            41698116222072977186158236678424689157993532961922,
            62467957194401269043877107275048102390895523597457,
            23189706772547915061505504953922979530901129967519,
            86188088225875314529584099251203829009407770775672,
            11306739708304724483816533873502340845647058077308,
            82959174767140363198008187129011875491310547126581,
            97623331044818386269515456334926366572897563400500,
            42846280183517070527831839425882145521227251250327,
            55121603546981200581762165212827652751691296897789,
            32238195734329339946437501907836945765883352399886,
            75506164965184775180738168837861091527357929701337,
            62177842752192623401942399639168044983993173312731,
            32924185707147349566916674687634660915035914677504,
            99518671430235219628894890102423325116913619626622,
            73267460800591547471830798392868535206946944540724,
            76841822524674417161514036427982273348055556214818,
            97142617910342598647204516893989422179826088076852,
            87783646182799346313767754307809363333018982642090,
            10848802521674670883215120185883543223812876952786,
            71329612474782464538636993009049310363619763878039,
            62184073572399794223406235393808339651327408011116,
            66627891981488087797941876876144230030984490851411,
            60661826293682836764744779239180335110989069790714,
            85786944089552990653640447425576083659976645795096,
            66024396409905389607120198219976047599490197230297,
            64913982680032973156037120041377903785566085089252,
            16730939319872750275468906903707539413042652315011,
            94809377245048795150954100921645863754710598436791,
            78639167021187492431995700641917969777599028300699,
            15368713711936614952811305876380278410754449733078,
            40789923115535562561142322423255033685442488917353,
            44889911501440648020369068063960672322193204149535,
            41503128880339536053299340368006977710650566631954,
            81234880673210146739058568557934581403627822703280,
            82616570773948327592232845941706525094512325230608,
            22918802058777319719839450180888072429661980811197,
            77158542502016545090413245809786882778948721859617,
            72107838435069186155435662884062257473692284509516,
            20849603980134001723930671666823555245252804609722,
            53503534226472524250874054075591789781264330331690]
    return str(reduce(op.add, [int(str(n)[0:12]) for n in nums]))[0:10]


@timeit
def p14(N1=1000000):
    """Which starting number, under one million, produces the longest
    chain in its Collatz sequence?
    """
    cnt = Counter()
    maxt = (1, 0)

    def collatz(N):
        dm = divmod(N, 2)
        return dm[0] if dm[1] == 0 else 3 * N + 1

    def count(N):
        if N > 1 and N not in cnt:
            cnt[N] += 1+count(collatz(N))
        return cnt[N]

    for n in range(2, N1+1):
        c = count(n)
        maxt = (n, c) if c > maxt[1] else maxt
    return maxt


@timeit
def p16(N=1000):
    return reduce(lambda x, y: int(x)+int(y), list(str(2**N)))


@timeit
def p17():
    # head-count occurences of unique words grouped according to frequency
    n = 891*len('and') + len('onethousand') + 900*len('hundred') \
        + 10*len('teneleventwelvethirteenfourteenfifteensixteenseventeeneighteennineteen') \
        + (90+100)*len('onetwothreefourfivesixseveneightnine') \
        + 100*len('twentythirtyfortyfiftysixtyseventyeightyninety')
    return n


@timeit
def p17alt(N=1000):
    if N > 1000:
        return 'N must be less than 1000!'
    digits = {0: 0, 1: len('one'), 2: len('two'), 3: len('three'), 4: len('four'), 5: len('five'),
              6: len('six'), 7: len('seven'), 8: len('eight'), 9: len('nine')}
    lst2 = {0: 0, 10: len('ten'), 11: len('eleven'), 12: len('twelve'), 13: len('thirteen'),
            14: len('fourteen'), 15: len('fifteen'), 16: len('sixteen'), 17: len('seventeen'),
            18: len('eighteen'), 19: len('nineteen')}
    tens = {0: 0, 1: 0, 2: len('twenty'), 3: len('thirty'), 4: len('forty'), 5: len('fifty'),
            6: len('sixty'), 7: len('seventy'), 8: len('eighty'), 9: len('ninety')}

    def countletters(n):
        if n == 1000:
            return len('onethousand')
        nletters = 0 if n < 100 or n % 100 == 0 else len('and')
        nletters = nletters + (digits[n/100] + len('hundred') if n >= 100 else 0)
        n = n % 100
        if n in lst2.keys():
            nletters = nletters + lst2[n]
        else:
            nletters = nletters + tens[n/10]
            n = n % 10
            if n > 0:
                nletters = nletters + digits[n]
        return nletters

    return sum([countletters(n) for n in range(1, N+1)])


@timeit
def p18(ptri=[[75], [95, 64], [17, 47, 82], [18, 35, 87, 10], [20, 4, 82, 47, 65], [19, 1, 23, 75, 3, 34], [88, 2, 77, 73, 7, 63, 67], [99, 65, 4, 28, 6, 16, 70, 92], [41, 41, 26, 56, 83, 40, 80, 70, 33], [41, 48, 72, 33, 47, 32, 37, 16, 94, 29], [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14], [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57], [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48], [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31], [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]]):
    nrows = len(ptri)
    for irow in reversed(range(0, nrows-1)):
        for icol, val in enumerate(ptri[irow]):
            childvals = [ptri[irow+1][icol], ptri[irow+1][icol+1]]
            ptri[irow][icol] = val + max(childvals)
    return ptri[0][0]


@timeit
def p67(fn='triangle.txt'):
    ptri = [[int(val) for val
            in line.replace('\n', '').split(' ')]
            for line in open(fn)]
    return p18(ptri)


@timeit
def p19():
    """Cheap or cheat?  Used existing calendar functionality.
    """
    def daterange(d0, d1):
        d1 = d1 + dt.timedelta(1)
        for n in range(int((d1-d0).days)):
            yield d0 + dt.timedelta(n)
    a = dt.date(1901, 1, 1)
    b = dt.date(2000, 12, 31)
    wdayson1st = [d.weekday() for d in daterange(a, b) if d.day == 1]
    return len([wday for wday in wdayson1st if wday == 6])


@timeit
def p20():
    return sum([int(digit) for digit in str(math.factorial(100))])


@timeit
def p21(N=10000):
    def sumdivs(n):
        s = 1
        i, nmax = 2, n
        while i <= nmax/i:
            if nmax%i == 0: s += i + (i != n/i)*n/i
            i += 1
        return s

    A = [0,0]+[sumdivs(i) for i in range(2,N)]
    return sum([i for i in range(2,N) if A[i] < N and A[A[i]]==i and A[i]!=i])


@timeit
def p21_fast(N=10000):
    A = list(nttools.sum_proper_divs(N))
    return sum([i for i in range(2,N) if A[i] < N and A[A[i]]==i and i!=A[i]])


@timeit
def p22():
    with open('names.txt') as f: names=sorted([n.strip('"') for n in f.read().split(',')])
    return sum(sum(ord(c)-64 for c in s)*i for i,s in enumerate(names,1))

@timeit
def p24():
    # works without islice([], n), but faster with it
    return list(islice(permutations(range(0, 10)), 1000000))[999999]


@timeit
def p25():
    for i, n in enumerate(nttools.gen_fib()):
        if len(str(n)) >= 1000:
            return (i, n)


@timeit
def p37():
    """The number 3797 has an interesting property. Being prime itself,
    it is possible to continuously remove digits from left to right,
    and remain prime at each stage: 3797, 797, 97, and 7. Similarly we
    can work from right to left: 3797, 379, 37, and 3.

    Find the sum of the only eleven primes that are both truncatable
    from left to right and right to left.
    """
    # subset: primes that start with 2, 3, 5, or 7;
    #         and ends in 3 or 7;
    #         and all digits odd
    # notes: * maybe create generator of numbers in subset if faster
    #          than the prime generator
    #        * or union of sets generated by the two generators
    isprime = lambda n: gmpy.mpz(n).is_prime() and nttools.pbr(n) == n
    return isprime(3838383)  # placeholder


@timeit
def p47(ndistinct=4, streak=4, Nmin=1000, Nmax=1000000):
    def consec(nums):
        for n in nums:
            if len(sp.primefactors(n)) != ndistinct:
                return False
        return True
    for i in range(Nmin, Nmax+1):
        if consec(range(i, i+streak)):
            return i
    return -1

@timeit
def p613():
    from scipy.integrate import dblquad
    from numpy import arctan2 as atan2
    from math import pi

    g = lambda x, y: (atan2(40-y, -x)-atan2(-y,30-x))/(2*pi*30*40/2.0)
    return dblquad(g, 0, 40, lambda x: 0, lambda x: 30-3.0/4*x,
                   epsabs = 1e-10)


# #####################################################################
# ################# PRELIMINARY ANALYSIS FUNCTIONS ####################
# #####################################################################


def p1_ana():
    # some observations about series of mult-3,5 numbers
    l1 = [i for i in range(0, 374) if i % 3 == 0 or i % 5 == 0]
    l2 = [i for i in range(3, 377) if i % 3 == 0 or i % 5 == 0]
    toadd = [x2 - x1 for x1, x2 in zip(l1, l2)]
    toadd2 = part(toadd, 7)
    msg = 'Notice the pattern of n(i+1)-n(i):'
    msglen = len(msg)
    print(msg + '\n' + ''.join(repeat('=', msglen)))
    seqstrlen = len(str(toadd2[0]))
    for n7 in toadd2:
        print(str("%%+%ds" % (msglen-(msglen-seqstrlen+2)/2)) % str(n7))
