#! /usr/bin/python

from sys import stdin, argv, stdout
from math import log as ln, exp

# Real test
submissions_per_test = 100
answers_per_submission = 10000

# scale model
#submissions_per_test = 10
#answers_per_submission = 20

log_file = stdout

def log( string ):
    log_file.write( " > %s\n" % string )

def read_test():
    result = []
    for i in range(submissions_per_test):
        result.append([ int(a) for a in stdin.readline().strip() ])
    return result

def question_probabilities( test ):
    result = []
    for i in range(answers_per_submission):
        right_answers = sum([ submission[i] for submission in test ])
        result.append( right_answers / submissions_per_test )
    return result

def sigmoid( x ):
    return 1 / ( 1 + exp(-x) )

def inverse_sigmoid( p ):
    # https://en.wikipedia.org/wiki/Logit
    if p == 0:
        return -3
    elif p == 1:
        return 3
    else:
        return ln( p / (1-p) )

def sigmoids( probabilities ):
    return [ sigmoid( p ) for p in probabilities ]

def inverse_sigmoids( probabilities ):
    return [ inverse_sigmoid( p ) for p in probabilities ]

def submission_scores( test ):
    result = []
    for i in range(submissions_per_test):
        result.append(sum( test[i] ))
    return result

def expected_score( skill, difficulties ):
    return sum([ sigmoid( skill - q ) for q in difficulties ])

def skills_by_score( difficulties ):
    mapping = {}
    for n in range( -300, 301 ):
        skill = n / 100
        mapping[ int(expected_score( skill, difficulties )) ] = skill
    result = []
    prev = -3
    for n in range( answers_per_submission + 1 ):
        try:
            prev = mapping[ n ]
            #log( "%s was present" % n )
        except KeyError:
            #log( "%s was missing" % n )
            mapping[ n ] = prev
        result.append( prev )
    return result

def submission_skills( test ):
    difficulties = inverse_sigmoids( question_probabilities( test ) )
    lookup_table = skills_by_score( difficulties )
    return [ lookup_table[ score ] for score in submission_scores( test ) ]

def entropy( submission, skill, difficulties ):
    result = 0
    for i in range( answers_per_submission ):
        q = difficulties[ i ]
        correct_probability = sigmoid( skill - q )
        answer = submission[ i ]
        if answer == 1:
            p = correct_probability
        else:
            # incorrect
            p = 1 - correct_probability
        nats = -p*ln(p)
        result += nats
    return result

def submission_entropies( test, difficulties, skills ):
    return [ entropy( test[i], skills[i], difficulties ) for i in range( submissions_per_test ) ]

def main():
    num_tests = int( stdin.readline().strip() )
    target_percentage = int( stdin.readline().strip() )
    for i in range( num_tests ):
        test = read_test()
        #print( "    Probabilities: %s" % question_probabilities( test ) )
        difficulties = inverse_sigmoids( question_probabilities( test ) )
        #print( "     Difficulties: %s" % difficulties )
        #print( "   Probabilities?: %s" % sigmoids( inverse_sigmoids( question_probabilities( test ) ) ) )
        #print( "Submission scores: %s" % submission_scores( test ) )
        #print( "  Skills by score: %s" % skills_by_score( difficulties ) )
        inferred_skills = submission_skills( test )
        #print( "Submission skills: %s" % inferred_skills )
        entropies = submission_entropies( test, difficulties, inferred_skills )
        #print( "Submission entropies: %s" % entropies )
        ordered_entropies = [ (entropies[i], i) for i in range(len( entropies )) ]
        ordered_entropies.sort()
        print( "Submission entropies: %s" % ordered_entropies )

main()
