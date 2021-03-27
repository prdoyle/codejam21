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

def main():
    num_tests = int( stdin.readline().strip() )
    for i in range( num_tests ):
        num_items = stdin.readline() # who cares
        test_case = stdin.readline().strip()
        cost = sorting_cost([ int(v) for v in test_case.split() ])
        print( "Case #%s: %s" % ( i+1, cost ) )

main()

#print( reverse( argv[3:], int(argv[1]), int(argv[2])) )
#print( sorting_cost( argv[1:] ) )
