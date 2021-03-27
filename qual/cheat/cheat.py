#! /usr/bin/python

from sys import stdin, argv

submissions_per_test = 10
answers_per_submission = 20

def read_test():
    result = []
    for i in range(submissions_per_test):
        result.append( stdin.readline().strip() )
    return result

def question_probabilities( test ):
    result = []
    for i in range(answers_per_submission):
        right_answers = sum([ submission[i] for submission in test ])
        result.append( right_answers / submissions_per_test )

def main():
    num_tests = int( stdin.readline().strip() )
    target_percentage = int( stdin.readline().strip() )
    for i in range( num_tests ):
        test = read_test()
        print( "Probabilities: %s" % question_probabilities( test ) )

main()
