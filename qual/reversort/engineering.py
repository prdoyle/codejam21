#! /usr/bin/python

from sys import stdin, argv

# i,j are 0-based
def reverse( numbers, i, j ):
    mid = numbers[ i : j+1 ]
    mid.reverse()
    return numbers[ :i ] + mid + numbers[ j+1: ]

def sorting_cost( numbers ):
    cost = 0
    for i in range( 0, len(numbers)-1 ):
        ( val, j ) = min([ ( numbers[idx], idx ) for idx in range( i, len(numbers) ) ])
        numbers = reverse( numbers, i, j )
        cost += j-i + 1
    return cost

def unsorted( num_items, target_cost, first_item ):
    if num_items <= 1:
        return [ first_item ] * num_items
    # If we left as little as possible for subsequent steps
    hero_cost = target_cost - ( num_items - 2 )
    # But we can't actually flip more than the whole sequence
    step_cost = min( num_items, hero_cost )
    # Get a list that eats up the remainder of target_cost
    suffix = unsorted( num_items-1, target_cost - step_cost, first_item+1 )
    # Apply a reversal with the desired step_cost
    result = [ first_item ] + suffix
    return reverse( result, 0, step_cost-1 )

def main():
    num_tests = int( stdin.readline().strip() )
    for i in range( num_tests ):
        ( num_items, target_cost ) = [ int(v) for v in stdin.readline().strip().split() ]
        min_cost = num_items - 1 # already in order
        max_cost = num_items * (num_items+1) // 2 - 1 # evens-then-odds; triangular number minus 1 because we don't "sort" the last item
        if target_cost < min_cost or target_cost > max_cost:
            solution = "IMPOSSIBLE"
        else:
            solution = unsorted( num_items, target_cost, 1 )
            solution = " ".join([ str(n) for n in solution ])
        print( "Case #%s: %s" % ( i+1, solution ) )

main()

#print( reverse( argv[3:], int(argv[1]), int(argv[2])) )
#print( sorting_cost( argv[1:] ) )
