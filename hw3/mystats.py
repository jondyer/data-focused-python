"""
@author: Jonathan Dyer & Brian Rhindress
2/3/2019
"""
# File: mystats.py
import numpy as np

# define the mean function here
def mean(a, *args):
    tot = 0
    length = 0
    for item in (a,) + args:
        try:
            iter(item)      # if we make it past this it's iterable
            tot += sum(item)
            length += len(item)
            
        except:             # otherwise just add the item
            tot += item
            length += 1
            
    return tot / length

# define the stddev function here
def stddev(a, *args):
    m = mean(a, args)
    length = 0
    tot = 0
    for item in (a,) + args:
        try:
            iter(item)      # if we make it past this it's iterable
            li = [i - m for i in item]
            li2 = [j**2 for j in li]
            
            tot += sum(li2)
            length += len(item)
            
        except:             # otherwise just use the item
            dev = item - m
            sq = dev**2
            
            tot += sq
            length += 1
            
    radicand = tot / (length - 1)
    
    return np.sqrt(radicand)


# define the median function here
def median(a, *args):
    li = []
    for item in (a,) + args:
        try:
            iter(item)      # if we make it past this it's iterable
            li.extend(item)
            
        except:             # otherwise just use the item
            li.append(item)
            
    li2 = sorted(li)
    
    if(len(li2) % 2 == 1):  # if length is odd
        return li2[len(li2) // 2]   # return the middle number
    else:                           # otherwise return avg of 2 middle nums
        val1 = li2[int(len(li2) / 2)]
        val2 = li2[int(len(li2) / 2) - 1]
        return mean(val1, val2)
    
# define the mode function here
def mode(a, *args):
    li = []
    for item in (a,) + args:
        try:
            iter(item)      # if we make it past this it's iterable
            li.extend(item)
            
        except:             # otherwise just use the item
            li.append(item)
    
    di = {i : li.count(i) for i in li}
    
    # get the largest value in the dict
    big = max(di.values())
    
    # and build the tuple of keys
    return tuple(i[0] for i in di.items() if i[1]==big)
    

if (__name__ == '__main__'):   
    # part (a)
    print('The current module is:', __name__)
    # output: "The current module is: __main__"
    
    # part (b)
    print('mean(1) should be 1.0, and is:', mean(1))
    print('mean(1,2,3,4) should be 2.5, and is:',
                                         mean(1,2,3,4))
    print('mean(2.4,3.1) should be 2.75, and is:',
                                         mean(2.4,3.1))
    # print('mean() should FAIL:', mean())
    
    # part (c)
    print('mean([1,1,1,2]) should be 1.25, and is:',
                                   mean([1,1,1,2]))
    print('mean((1,), 2, 3, [4,6]) should be 3.2, ' +
          'and is:', mean((1,), 2, 3, [4,6]))
    
    # part (d)
    for i in range(10):
        print("Draw", i, "from Norm(0,1):",
              np.random.randn())
    
    ls50 = [np.random.randn() for i in range(50)]
    print("Mean of", len(ls50), "values from Norm(0,1):",
          mean(ls50))
    
    ls10000 = [np.random.randn() for i in range(10000)]
    print("Mean of", len(ls10000), "values from " +
          "Norm(0,1):", mean(ls10000))
    
    # part (e)
    np.random.seed(0)
    a1 = np.random.randn(10)
    print("a1:", a1)    # should display an ndarray of 10 values
    
    print("the mean of a1 is:", mean(a1))
    
    
    # part (f)
    print("the stddev of a1 is:", stddev(a1))
    
    # part (g)
    print("the median of a1 is:", median(a1))
    print("median(3, 1, 5, 9, 2):", median(3, 1, 5, 9, 2))
    
    # part (h)
    print("mode(1, 2, (1, 3), 3, [1, 3, 4]) is:",
          mode(1, 2, (1, 3), 3, [1, 3, 4]))
