# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from sets import Set
from PIL import Image
import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        print 'Solving ' + problem.name
        
        # Get the matrix items
        matrix = self.get_matrix(problem)
        
        # Check if all of the items are the same
        if self.check_if_all_are_same(matrix):
            print 'all are same'
            return 0;
            #find the same one

        return 1;
        
    def get_matrix(self, problem):
        return {k: v for k, v in problem.figures.iteritems() if k.isalpha()}

    def check_if_all_are_same(self, matrix):
        set = []
    
        for figureName in matrix:
            thisFigure = matrix[figureName]
            
            for objectName in thisFigure.objects:
                thisObject = thisFigure.objects[objectName]
                set.append(thisObject.attributes)

        print set
        return True