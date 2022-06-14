import random
import string

#I chose a simple algorithm, to map a full_url to a random string at the length
#of 8, which appears to provide enough permutations
def shorten_url():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=8))