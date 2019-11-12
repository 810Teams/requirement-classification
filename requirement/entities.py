from math import floor

class RequirementData():
    '''
        Class: RequirementGroup
        Purpose: Contains title and all requirements that have been submitted by user
    '''
    def __init__(self, title, requirements):
        self.title = title                                                     # Type: String
        self.requirements = [Requirement(i) for i in requirements.split('\n')] # Type: List<Requirement>

class Requirement():
    '''
        Class: Requirement
        Purpose: Contains data of a single requirement
    '''
    def __init__(self, description):
        self.description = description # Type: String
        self.rating = None             # Type: Integer

    def set_rating(self, rating):
        self.rating = floor(min(max(0, rating), 10))

class RequirementGroup():
    '''
        Class: RequirementGroup
        Purpose: Contains main requirement and its related ones
    '''
    def __init__(self, main, chained):
        self.main = main       # Type: Requirement
        self.chained = chained # Type: List<Requirement>
