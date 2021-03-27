#! /usr/bin/python

from sys import stdin, argv, stdout
from math import log as ln, exp
import random

# Real test
submissions_per_test = 100
answers_per_submission = 10000

# scale model
#submissions_per_test = 10
#answers_per_submission = 20

log_file = stdout

def log( string ):
    pass
    #log_file.write( " > %s\n" % string )

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

def surprise( submission, skill, difficulties ):
    nats = []
    for i in range( answers_per_submission ):
        q = difficulties[ i ]
        correct_probability = sigmoid( skill - q )
        answer = submission[ i ]
        if answer == 1:
            p = correct_probability
        else:
            # incorrect
            p = 1 - correct_probability
        nats.append( -ln(p) )
    return max( nats )

def submission_surprises( test, difficulties, skills ):
    return [ surprise( test[i], skills[i], difficulties ) for i in range( submissions_per_test ) ]

def hard_questions( test ):
    prob_limit = 0.1
    qp = question_probabilities( test )
    return [ i for i in range( answers_per_submission ) if qp[i] <= prob_limit ]

def question_band( test, min_prob, max_prob ):
    qp = question_probabilities( test )
    return [ i for i in range( answers_per_submission ) if min_prob <= qp[i] <= max_prob ]

def subset_score( test, subset ):
    return [ sum([ submission[i] for i in subset ]) for submission in test ]

def top_scoring_submission_on_subset( test, subset ):
    s = subset_score( test, subset )
    ( score, result ) = max([ ( s[i], i ) for i in range( submissions_per_test ) ])
    return result

def cheat_off( test ):
    log( "Cheat off!" )
    scores = [0] * submissions_per_test
    hq = hard_questions( test )
    for r in range(1, 21):
        log( " | Round %s" % r )
        subset = random.sample( hq, len(hq)//10 )
        log( " |   Subset: %s" % subset )
        winner = top_scoring_submission_on_subset( test, subset )
        log( " |   Winner: %s" % winner )
        scores[ winner ] += 1
    ordered_scores = [ ( scores[i], i ) for i in range( submissions_per_test ) ]
    ordered_scores.sort()
    ( score, result ) =  ordered_scores[-1]
    log( " | CHAMPION IS %s" % result )
    return result;

def main():
    num_tests = int( stdin.readline().strip() )
    target_percentage = int( stdin.readline().strip() )
    for i in range( num_tests ):
        test = read_test()
        #print( "    Probabilities: %s" % question_probabilities( test ) )
        #difficulties = inverse_sigmoids( question_probabilities( test ) )
        #print( "     Difficulties: %s" % difficulties )
        #print( "   Probabilities?: %s" % sigmoids( inverse_sigmoids( question_probabilities( test ) ) ) )
        #print( "  Skills by score: %s" % skills_by_score( difficulties ) )
        #inferred_skills = submission_skills( test )
        #print( "Submission skills: %s" % inferred_skills )
        #surprises = submission_surprises( test, difficulties, inferred_skills )
        #print( "Submission surprises: %s" % surprises )
        #ordered_surprises = [ (surprises[i], i) for i in range(len( surprises )) ]
        #ordered_surprises.sort()
        #print( "Submission surprises: %s" % ordered_surprises )
        #aqs = submission_scores( test ) # All-question score
        #print( "Submission scores: %s" % [ (aqs[i], i ) for i in range( submissions_per_test ) ] )
        #the_hard_questions = hard_questions( test )
        #print( "Hard questions: %s %s" % ( len(the_hard_questions), the_hard_questions ) )
        #hqs = subset_score( test, the_hard_questions )  # Hard-question score
        #print( "Hard question scores: %s %s" % ( len(hqs), [ (hqs[i], i) for i in range( submissions_per_test ) ] ) )
        #ordered_hard_questions = [ ( hqs[i], i ) for i in range( submissions_per_test ) ]
        #ordered_hard_questions.sort()
        #print( "Hard questions ordered: %s" % ordered_hard_questions )
        #hard_question_quotients = [ ( max(1, aqs[i]) / max(1,hqs[i]), i ) for i in range( submissions_per_test ) ]
        #hard_question_quotients.sort()
        #log( "Hard question quotients: %s" % hard_question_quotients )
        #( q, cheater ) = hard_question_quotients[0]
        cheater = cheat_off( test )
        print( "Case #%s: %s" % ( i+1, cheater+1 ) )

main()
