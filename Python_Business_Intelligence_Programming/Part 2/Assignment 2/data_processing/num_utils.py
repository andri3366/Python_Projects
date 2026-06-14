
def round_num(num, n):
    
    return round(num, n)

def avgerage(nums):
    
    if not nums:
        return 0
    return sum(nums) / len(nums)

def frac_part(num):
    
    if num is not float:
        return 0
    
    return num - int(num)