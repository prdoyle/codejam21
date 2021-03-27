#! /usr/bin/python

from sys import argv, stdin

def parse_sequence( sequence_string ):
    #sequence_separators = sequence_string.lower().split( "?" )
    # Blank separators are not significant. There's no reason to flip C/J in the middle of a string of "????"
    #return [ s for s in sequence_separators if s ]
    return sequence_string.replace("?","").lower()

def min_cost( x, y, seq ):
    cost = 0
    for i in range( len(seq)-1 ):
        transition = seq[i:i+2]
        if transition == "cj":
            cost += x
        elif transition == "jc":
            cost += y
    return cost

def main():
    num_tests = int( stdin.readline().strip() )
    for i in range( num_tests ):
        ( x, y, sequence_string ) = stdin.readline().strip().split( None, 2 )
        seq = parse_sequence( sequence_string )
        print( "Case #%d: %d" % ( i+1, min_cost( int(x), int(y), seq ) ) )

#print( min_cost( int(argv[1]), int(argv[2]), parse_sequence( argv[3] )) )
main()
