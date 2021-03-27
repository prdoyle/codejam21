#! /usr/bin/python

from sys import stdin, stdout, stderr, argv

log_file = open( "log.mediansort", "a" )
log_file.write( "\n------------------\n" )
def log( string ):
    pass
    #log_file.write( " > %s\n" % string )

def median_sorted( num_elements, median_of ):
    if num_elements <= 2:
        # Doesn't matter
        return [ i+1 for i in range( num_elements ) ]
    else:
        n = num_elements
        sublist = median_sorted( n-1, median_of )
        insertion_point = ternary_search( sublist, n, 0, n-2, median_of )
        return sublist[ : insertion_point ] + [ n ] + sublist[ insertion_point : ]

def ternary_search( sublist, n, lo, hi, median_of ):
    """Returns zero-based index between lo and hi (inclusive) at which the number n should be inserted"""
    log( "ternary_search( %s, %s, %s )" % ( sublist, lo, hi ) )
    if hi-lo < 5:
        # Who wants to think about corner cases for small lists?
        log( " | j/k, let's do linear search" )
        result = linear_search( sublist, n, lo, hi, median_of )
        log( " | result = %s" % result )
        return result
    else:
        new_lo = ( 2*lo + hi ) // 3
        new_hi = ( 2*hi + lo ) // 3
        subscript_lo = sublist[ new_lo ]
        subscript_hi = sublist[ new_hi ]
        log( " | new_lo=%s new_hi=%s subscript_lo=%s subscript_hi=%s" % ( new_lo, new_hi, subscript_lo, subscript_hi ) )
        median = median_of( subscript_lo, n, subscript_hi )
        if median == subscript_lo:
            log( " | under" )
            return ternary_search( sublist, n, lo, new_lo-1, median_of )
        elif median == subscript_hi:
            log( " | over" )
            return ternary_search( sublist, n, new_hi+1, hi, median_of )
        else:
            log( " | between" )
            return ternary_search( sublist, n, new_lo, new_hi, median_of )

def linear_search( sublist, n, lo, hi, median_of ):
    """sublist is a list of subscripts known to be sorted. n is a new subscript to add in there. lo and hi are zero-based indexes into sublist"""
    log( "linear_search( %s, %s, %s )" % ( sublist, lo, hi ) )
    if lo == hi:
        # Corner case: if hi == lo they refer to the same item, and we 
        # can't tell them apart, making our whole algorithm break down!
        # Just bump one of them
        if lo >= 1:
            log( "| widen lo=%s" % lo )
            lo -= 1
        else:
            log( "| widen hi=%s" % hi )
            hi += 1
    subscript_lo = sublist[ lo ]
    subscript_hi = sublist[ hi ]
    median = median_of( subscript_lo, n, subscript_hi )
    if median == subscript_lo:
        log( "| under %s" % lo )
        return lo
    elif median == subscript_hi:
        log( "| over %s" % hi )
        return hi+1
    elif hi - lo == 1:
        log( "| snug %s" % hi )
        return hi
    else:
        log( "| recurse" )
        return linear_search( sublist, n, lo+1, hi-1, median_of )

def stdout_median( *subscripts ):
    log( "ASK: %s" % ( subscripts, ) )
    print( " ".join([ str(n) for n in subscripts ]) )
    stdout.flush()
    result = int( stdin.readline().strip() )
    log( " | Answer: %s" % result )
    if result == -1:
        raise ValueError # Judge has spoken
    elif not result in subscripts:
        raise AssertionError # Judge lied
    return result

def mock_median_function( values ):
    def median( *args ):
        #log( "  median(%s)" % args )
        subset = [ ( values[i-1], i ) for i in args ]
        ( _, result ) = sorted( subset )[1]
        #log( "  | subset %s -> %s" % ( subset, result ) )
        return result
    return median

def main():
    parameters = [ int(v) for v in stdin.readline().strip().split() ]
    log( "Parameters: T=%s N=%s Q=%s" % tuple(parameters) )
    [ num_tests, num_elements, question_budget ] = parameters
    for i in range( num_tests ):
        result = median_sorted( num_elements, stdout_median )
        log( "SOLUTION: %s" % result )
        print( " ".join([ str(n) for n in result ]) )
        stdout.flush()
        if stdin.readline().strip() != "1":
            raise ValueError # Wrong answer

def test():
    numbers = [ int(v) for v in argv[1:] ]
    print(median_sorted( len(numbers), mock_median_function( numbers ) ))

main()
#test()
stdout.flush()
