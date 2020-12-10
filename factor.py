import math
import time

def factor(num): #12
    ans = []
    
    while num % 2 == 0:
        ans.append(2)
        num /= 2
        
    for odd in range(3, int(num)+1, 2):
        while num % odd == 0:
            ans.append(odd)
            num /= odd
            
    return [] if len(ans) == 1 else ans

#for verifying purpose only
def get_prime_numbers(num):
    if num < 2:
        return []
    ans = [2]
    for n in range(3, num+1, 2):
        ans.append(n)
        
        i = 1
        multiply = ans[1]
        while multiply * multiply <= n:
            if n%multiply == 0:
                ans.remove(n)
                break
            i += 1
            multiply = ans[i]
    return ans

def verify(expected_product, prime_factors):
    isprime = expected_product in get_prime_numbers(expected_product)
    actual_product = 1
    for factor in prime_factors:
        actual_product *= factor
    
    if isprime:
        return  prime_factors == []
    return expected_product == actual_product

def performance(num):
    start = time.time()
    factor(num)
    end = time.time()
    return end-start

print("factor of 7748 is: ", factor(7748))
print("verify 7748 is: ", verify(7748, factor(7748)))
print("factorization performance of 7748 is: ", performance(7748))

