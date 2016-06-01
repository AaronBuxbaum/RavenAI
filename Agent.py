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
#import numpy
import json

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
        options = self.get_options(problem)

        # Get the difference between A and C
        diff = self.get_diff(matrix, 'A', 'C')

        # If A equals C, then D must equal B
        if diff == 'No difference':
            return self.find_equal(matrix['B'], options)

        if diff == 'Different number of objects':
            return -1
        
        # Compare semantic networks
        for transform in diff:
            if transform == 'angle':
                rotation = int(diff[transform][0]) - int(diff[transform][1])

        for objectKey in matrix['B'].objects:
            matrix['B'].objects[objectKey].attributes['angle'] = str((int(matrix['B'].objects[objectKey].attributes['angle']) + rotation) % 360)
        
        return self.find_equal(matrix['B'], options)
        
    def get_diff(self, matrix, a, b):
        objA = self.get_objects(matrix[a])
        objB = self.get_objects(matrix[b])
        if len(objA) != len(objB):
            return 'Different number of objects'
        if objA == objB:
            return 'No difference'

        dictA = json.loads(objA[0])
        dictB = json.loads(objB[0])
        diff = {}
        for k in dictA.viewkeys() & dictB.viewkeys():
            if dictA[k] != dictB[k]:
                diff[k] = [dictA[k], dictB[k]]
        return diff

    def get_matrix(self, problem):
        return {k: v for k, v in problem.figures.iteritems() if k.isalpha()}

    def get_options(self, problem):
        return {k: v for k, v in problem.figures.iteritems() if k.isalpha() == False}
        
    def find_equal(self, comparator, options):
        for option in options:
            possibleAnswer = options[option]
            if self.get_objects(comparator) == self.get_objects(possibleAnswer):
                return int(option)
        return -1
        
    def get_objects(self, object):
        arr = []
        for objectName in object.objects:
            thisObject = object.objects[objectName]
            arr.append(json.dumps(thisObject.attributes))
        return arr