''IS 211 ASSIGNMENT ONE''

def list_divide(numbers, divide=2):
    divisible_count = 0
    for every_num in numbers:
        if every_num % divide == 0:
            divisible_count += 1
    return divisible_count

class ListDivideException(Exception):
    pass

def test_list_divide():
    try:
        if not list_divide([1,2,3,4,5]) == 2:
            raise ListDivideException
        if not list_divide([2,4,6,8,10]) == 5:
            raise ListDivideException
        if not list_divide([30,54,63,98,100], divide=10) == 2:
            raise ListDivideException
        if not list_divide([]) == 0:
            raise ListDivideException
        if not list_divide([1,2,3,4,5], 1) == 5:
            raise ListDivideException
        print("All test cases passed")
    except ListDivideException:
        print("Division exception occurred")

test_list_divide()
