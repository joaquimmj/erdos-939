"""support-restricted search: each known r = 5 solution is found from its own prime set, and from no smaller one"""
from search_r5_wide import search
from rpow import rpowerful, primes_upto
if __name__ == '__main__':
    K = (772402208, 1977326743, 134481277728, 137231006679); C = (11**5 * 13**5, 2**12 * 23**6, 2**8 * 3**10 * 5**7, 3**7 * 61**5)
    assert search(5, 10**13, workers=2, primes=[2, 3, 7, 13, 17])[0] == [K]
    assert search(5, 10**13, workers=2, primes=[2, 3, 5, 11, 13, 23, 61])[0] == [C]
    assert search(5, 10**13, workers=2, primes=[2, 3, 5, 7, 11, 13, 17, 19, 23])[0] == [K]
    assert search(5, 10**13, workers=2, primes=[2, 3, 7, 13])[0] == []
    assert rpowerful(5, 10**9, primes_upto(63)) == rpowerful(5, 10**9)      # 64^5 > 1e9: same list
    print('support tests OK')
