from math import floor

from requirement.analyze import *

class RequirementData():
    '''
        Class: RequirementData
        Purpose: Contains title and all requirements that have been submitted by user
    '''
    def __init__(self, title, requirements):
        self.title = title # Type: String

        # Type: List<Requirement>
        if isinstance(requirements, list):
            for i in range(len(requirements)):
                if isinstance(requirements[i], str):
                    requirements[i] = Requirement(requirements[i].replace('\n', ''))
            self.requirements = requirements
        elif isinstance(requirements, str):
            self.requirements = [Requirement(i) for i in requirements.split('\n')]

        self.by_priority = self.analyze_priority()           # Type: RequirementPriorityGroup
        self.by_functionality = self.analyze_functionality() # Type: RequirementFunctionalityGroup
        self.by_keyword = self.analyze_keyword()             # Type: RequirementKeywordGroup

    def analyze_priority(self):
        response = get_data_group_by_priority([i.description for i in self.requirements])
        return RequirementPriorityGroup(response[0], response[1], response[2])

    def analyze_functionality(self, requirements):
        response = get_data_group_by_functionality([i.description for i in self.requirements])
        return RequirementFunctionalityGroup(response[0], response[1])

    def analyze_keyword(self, requirements):
        response = get_data_group_by_keyword([i.description for i in self.requirements])
        return [RequirementKeywordGroup(i, response[i]) for i in response]

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

class RequirementRelatedGroup():
    '''
        Class: RequirementRelatedGroup
        Purpose: Contains main requirement and its related ones
    '''
    def __init__(self, main, chained):
        self.main = main       # Type: Requirement
        self.chained = chained # Type: List<Requirement>

class RequirementPriorityGroup():
    '''
        Class: RequirementPriorityGroup
        Purpose: Contains requirements grouped in priority levels
    '''
    def __init__(self, high, medium, low):
        self.high = high     # Type: List<Requirement>
        self.medium = medium # Type: List<Requirement>
        self.low = low       # Type: List<Requirement>

class RequirementFunctionalityGroup():
    '''
        Class: RequirementFunctionalityGroup
        Purpose: Contains requirements grouped in functionality
    '''
    def __init__(self, functional, non_functional):
        self.functional = functional         # Type: List<Requirement>
        self.non_functional = non_functional # Type: List<Requirement>

class RequirementKeywordGroup():
    '''
        Class: RequirementKeywordGroup
        Purpose: Contains requirements related to a certain keyword
    '''
    def __init__(self, keyword, requirements):
        self.keyword = keyword           # Type: String
        self.requirements = requirements # Type: List<Requirement>
