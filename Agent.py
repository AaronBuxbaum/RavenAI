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
import random

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
        comparisons = self.build_comparisons(figures)
        comparisons = self.weight_comparisons(comparisons)
        comparisons = sorted(comparisons.items(), key=lambda x: x[1])
        i = 0
        for item in comparisons:
            if item[1] == comparisons[0][1]:
                i = i + 1
        return int(random.choice(comparisons[0:i])[0])
        
   
    # Compare all possible comparisons to the comparator
    def build_comparisons(self, figures):
        comparator = self.diff_figures(figures, 'A', 'C')  # Create a baseline comparison
        comparisons = {}
        
        options = self.get_options(figures)
        for option in sorted(options):
            diff = self.diff_figures(figures, 'B', option)
            comparison = self.diff_diffs(comparator, diff)
            comparisons[option] = comparison
        return comparisons
        
        
    def weight_comparisons(self, comparisons):
        for i in comparisons:
            comparison = comparisons[i]
            value = 0

            for diff in comparison:
                for attr in diff:
                    value = value + 5
                    if type(attr) == list and None in attr:
                        value = value + 10
                    if attr == 'angle':
                        value = value + 1
                    elif attr == 'alignment':
                        value = value + 2
                    elif attr == 'shape':
                        value = value + 3
            comparisons[i] = value
        return comparisons
            
    
    def diff_figures(self, figures, a, b):
        differences = [];
        while len(figures[b].objects) > len(figures[a].objects):
            differences.append({'object': 'Added'})
            figures[b].objects.pop(sorted(figures[b].objects)[0])
        while len(figures[a].objects) > len(figures[b].objects):
            differences.append({'object': 'Removed'})
            figures[a].objects.pop(sorted(figures[a].objects)[0])
        for i,j in zip(sorted(figures[a].objects), sorted(figures[b].objects)):
            objectA = figures[a].objects[i].attributes
            objectB = figures[b].objects[j].attributes
            differences.append(self.diff_objects(objectA, objectB))
        return differences

            
    def diff_objects(self, obj1, obj2):
        differences = {}
        for attribute in obj1.viewkeys() | obj2.viewkeys():
            if attribute not in obj1:
                obj1[attribute] = None
            if attribute not in obj2:
                obj2[attribute] = None
            if obj1[attribute] != obj2[attribute]:
                difference_observed = self.handle_difference(attribute, obj1[attribute], obj2[attribute])
                if difference_observed is not None:
                    differences[attribute] = difference_observed
        return differences
        
        
    def diff_diffs(self, diff1, diff2):
        differences = []
        for a,b in zip(diff1, diff2):
            differences.append(self.diff_objects(a, b))
        return differences
        

    def handle_difference(self, attribute, a, b):
        if attribute == 'angle':
            a = a or 0
            b = b or 0
            return (int(a) + int(b)) % 360
        elif attribute == 'fill':
            return a == b
        elif attribute == 'inside':
            return None
        elif attribute == 'alignment':
            a = a or 'none-none'
            b = b or 'none-none'
            
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