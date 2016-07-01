import random
import numpy
from PIL import Image, ImageChops

class Agent:
    def __init__(self):
        pass

    def Solve(self, problem):
        print 'Solving ' + problem.name
        return self.find_best_match(problem)


    def find_best_match(self, problem):
        figures = problem.figures
        problemType = problem.problemType
        comparator_figures = self.get_comparator_figures(problemType)

        if problem.hasVerbal:
            comparisons = self.build_comparisons(figures, comparator_figures)
            comparisons = self.weight_comparisons(comparisons)
            comparisons = sorted(comparisons.items(), key=lambda x: x[1])
            number_of_matches = self.get_match_number(comparisons)
            return self.select_random_from_slice(comparisons, number_of_matches)

        else:
            comparator = self.get_root_mean_square(self.get_histogram_from_images(figures, comparator_figures[0], comparator_figures[1]))
            possible_answers = []
            for option in sorted(self.get_options(figures)):
                compare = self.get_root_mean_square(self.get_histogram_from_images(figures, comparator_figures[2], str(option)))
                possible_answers.append(compare)
            return numpy.abs(numpy.subtract.outer(possible_answers, comparator)).argmin() + 1

    def get_histogram_from_images(self, figures, a, b):
        im1 = Image.open(figures[a].visualFilename)
        im2 = Image.open(figures[b].visualFilename)
        return ImageChops.difference(im1, im2).histogram()

    # Calculate similarity between two images with root mean square.
    def get_root_mean_square(self, arr):
        return numpy.sqrt(numpy.mean(numpy.square(arr)))

    # Compare all possible comparisons to the comparator
    def build_comparisons(self, figures, comparator_figures):
        comparator = self.diff_figures(figures, comparator_figures[0], comparator_figures[1])
        comparisons = {}

        options = self.get_options(figures)
        for option in sorted(options):
            diff = self.diff_figures(figures, comparator_figures[2], option)
            comparison = self.diff_diffs(comparator, diff)
            comparisons[option] = comparison
        return comparisons


    def get_comparator_figures(self, problemType):
        if problemType == '2x2':
            return ['A', 'C', 'B']
        else:
            return ['E', 'F', 'H']


    def weight_comparisons(self, comparisons):
        for i in comparisons:
            comparison = comparisons[i]
            value = 0
            for diff in comparison:
                for attr in diff:
                    value = value + 5
                    if attr == 'shape':
                        value = value + 1
                    if attr == 'size':
                        value = value + abs(diff[attr])
            comparisons[i] = value
        return comparisons


    def diff_figures(self, figures, a, b):
        differences = [];
        i = len(figures[b].objects) - len(figures[a].objects)
        while i is not 0:
            if i > 0:
                differences.append({object: 'Added'})
                i = i-1
            if i < 0:
                differences.append({object: 'Removed'})
                i = i+1
        for i,j in zip(reversed(sorted(figures[a].objects)), reversed(sorted(figures[b].objects))):
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
        if attribute == 'size':
            a = a or 0
            b = b or 0
            try:
                if int(a) and int(b):
                    return a - b
            except:
                sizes = [0, 'very small', 'small', 'medium', 'large', 'very large', 'huge']
                return int(sizes.index(a) - sizes.index(b))
        elif attribute == 'angle':
            a = a or 0
            b = b or 0
            return (int(a) + int(b)) % 360
        elif attribute == 'fill':
            return a == b
        elif attribute in ['inside', 'left-of', 'above', 'overlaps', 'right-of', 'top-of', 'bottom-of', 'outside']:
            a = a or ""
            b = b or ""
            #return [len(str(a).split(",")), len(str(b).split(","))]
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

    def get_match_number(self, comparisons):
        i = 0
        for item in comparisons:
            if item[1] == comparisons[0][1]:
                i = i + 1
        return i


    def select_random_from_slice(self, comparisons, number_of_matches):
        if number_of_matches == len(comparisons):
            return -1
        return int(random.choice(comparisons[0:number_of_matches])[0])


    def get_options(self, figures):
        return {k: v for k, v in figures.iteritems() if k.isalpha() == False}