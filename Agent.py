# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

#from PIL import Image
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
        return self.find_best_match(problem.figures)


    def find_best_match(self, figures):
        # TODO: handle multiple objects
        if len(figures['A'].objects) > 1:
            return -1
        
        comparisons = self.build_comparisons(figures)
        comparisons = self.weight_comparisons(comparisons)
        return comparisons[0]['id']
        
   
    # Compare all possible comparisons to the comparator
    def build_comparisons(self, figures):
        comparator = self.diff_figures(figures, 'A', 'C')  # Create a baseline comparison
        comparisons = []
        options = self.get_options(figures)
        for option in options:
            diff = self.diff_figures(figures, 'B', option)
            comparison = self.diff_objects(comparator, diff)
            comparison['id'] = int(option)
            comparisons.append(comparison)
        return comparisons
        
        
    def weight_comparisons(self, comparisons):
        for comparison in comparisons:
            value = 0
            for attribute in comparison:
                value = value + 5
                if type(comparison[attribute]) == list and None in comparison[attribute]:
                    value = value + 10
                if attribute == 'angle':
                    value = value + 1
                elif attribute == 'alignment':
                    value = value + 2
                elif attribute == 'shape':
                    value = value + 3
            comparison['value'] = value
        return sorted(comparisons, key=lambda x: x['value'])
            
    
    def diff_figures(self, figures, a, b):
        objectA = figures[a].objects[figures[a].objects.keys()[0]].attributes
        objectB = figures[b].objects[figures[b].objects.keys()[0]].attributes
        return self.diff_objects(objectA, objectB)

            
    def diff_objects(self, diff1, diff2):
        differences = {}
        for attribute in diff1.viewkeys() | diff2.viewkeys():
            if attribute not in diff1:
                diff1[attribute] = None
            if attribute not in diff2:
                diff2[attribute] = None
            if diff1[attribute] != diff2[attribute]:
                differences[attribute] = self.handle_difference(attribute, diff1[attribute], diff2[attribute])
        return differences
        

    def handle_difference(self, attribute, a, b):
        if attribute == 'angle':
            if a == None:
                a = 0
            if b == None:
                b = 0
            return ((int(a) + int(b)) % 360)
        elif attribute == 'alignment':
            if a == None:
                a = 'none-none'
            if b == None:
                b = 'none-none'
            
            first = a.split('-')
            second = b.split('-')
            
            # assume just top/bottom and left/right
            relativeAlignment = []
            for i in range(len(first)):
                if first[i] == second[i]:
                    relativeAlignment.append('equal')
                else:
                    relativeAlignment.append('flip')
            return '-'.join(relativeAlignment)
        else:
            return [a, b]
        
        
    def get_options(self, figures):
        return {k: v for k, v in figures.iteritems() if k.isalpha() == False}