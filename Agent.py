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
        # Otherwise, apply transformation to B to find D
        for attribute in diff:
            transform = diff[attribute]
            if attribute == 'angle':
                rotation = int(transform[0]) - int(transform[1])
                if attribute not in matrix['B'].objects['b'].attributes:
                    matrix['B'].objects['b'].attributes[attribute] = 0
                matrix['B'].objects['b'].attributes[attribute] = str((int(matrix['B'].objects['b'].attributes[attribute]) + rotation) % 360)
            elif attribute == 'fill':
                matrix['B'].objects['b'].attributes[attribute] = diff[attribute][1]
            elif attribute == 'shape':
                matrix['B'].objects['b'].attributes[attribute] = diff[attribute][1]
            elif attribute == 'alignment':
                matrix['B'].objects['b'].attributes[attribute] = diff[attribute][1]
            else:
                print attribute

        return self.find_best_match(matrix['B'], options)



    # TODO
    def handle_difference(self, attribute, a, b):
        possible_attributes = ['shape', 'size', 'fill', 'angle', 'alignment']
        return [a, b]
        
        
        
    # TODO: handle multiple objects
    def get_diff(self, matrix, a, b):        

        differences = {}
        objectA = matrix[a].objects[a.lower()].attributes
        objectB = matrix[b].objects[b.lower()].attributes
        
        for attribute in objectA.viewkeys() & objectB.viewkeys():
            if objectA[attribute] != objectB[attribute]:
                differences[attribute] = self.handle_difference(attribute, objectA[attribute], objectB[attribute])
                
        return differences
        
        
    # TODO: rewrite, allow some gray area
    def find_best_match(self, comparator, options):
        for option in options:
            possibleAnswer = options[option]
            if self.get_objects(comparator) == self.get_objects(possibleAnswer):
                return int(option)
        return -1
        
        
        

    def get_matrix(self, problem):
        return {k: v for k, v in problem.figures.iteritems() if k.isalpha()}

    def get_options(self, problem):
        return {k: v for k, v in problem.figures.iteritems() if k.isalpha() == False}
        
    def get_objects(self, object):
        arr = []
        for objectName in object.objects:
            thisObject = object.objects[objectName]
            arr.append(json.dumps(thisObject.attributes))
        return arr