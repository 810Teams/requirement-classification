from math import floor

from pythainlp.corpus.common import thai_words
from pythainlp.tag import pos_tag
from pythainlp import Tokenizer


class RequirementData():
    '''
        Class: RequirementData
        Purpose: Contains title and all requirements that have been submitted by user
    '''
    def __init__(self, title, requirements):
        self.title = title # Type: String

        if isinstance(requirements, str):
            requirements = [i.strip() for i in requirements.split('\n')]
        for i in range(len(requirements)):
            requirements[i] = Requirement(i + 1, requirements[i].replace('\n', ''))

        self.requirements = requirements                     # Type: List<Requirement>
        self.by_priority = self.analyze_priority()           # Type: RequirementPriorityGroup
        self.by_functionality = self.analyze_functionality() # Type: RequirementFunctionalityGroup
        self.by_keyword = self.analyze_keyword()             # Type: RequirementKeywordGroup

    def analyze_priority(self):
        response = get_data_group_by_priority(self.requirements)
        return RequirementPriorityGroup(response[0], response[1], response[2])

    def analyze_functionality(self):
        response = get_data_group_by_functionality(self.requirements)
        return RequirementFunctionalityGroup(response[0], response[1])

    def analyze_keyword(self):
        response = get_data_group_by_keyword(self.requirements)
        return [RequirementKeywordGroup(i, response[i]) for i in response]

class Requirement():
    '''
        Class: Requirement
        Purpose: Contains data of a single requirement
    '''
    def __init__(self, id, description):
        self.id = id                   # Type: Integer
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

class Keyword():
    '''
        Class: Keyword
        Purpose: Contains data of keyword
    '''
    def __init__(self, word, weight):
        self.word = word     # Type: String
        self.weight = weight # Type: Integer

WORDS = set(thai_words())
_ = [WORDS.add(i.replace('\n', '').strip()) for i in open('requirement/data/custom_tokenizer.txt')]
TOKENIZER = Tokenizer(WORDS)

KEYWORDS_HIGH_PRIORITY = [
    Keyword('เด็ดขาด', 2),
    Keyword('ต้อง', 2),
    Keyword('จำเป็น', 2),
    Keyword('ห้าม', 2),
    Keyword('ไม่มีไม่ได้', 2),
]

KEYWORDS_MEDIUM_PRIORITY = [
    Keyword('อยาก', 2),
    Keyword('ควร', 2),
    Keyword('น่าจะ', 2),
    Keyword('เอา', 2),
    Keyword('ได้', 1),
]

KEYWORDS_LOW_PRIORITY = [
    Keyword('แต่ไม่', 2),
    Keyword('ถึงแม้', 2),
    Keyword('ถึงไม่', 2),
    Keyword('ไม่เป็นไร', 2),
    Keyword('ไม่เป็นอะไร', 2),
    Keyword('อะไรก็ได้', 2),
    Keyword('ชอบ', 2),
    Keyword('ก็ได้', 1),
    Keyword('ก็ดี', 1),
    Keyword('สี', 1),
    Keyword('รูป', 1),
    Keyword('ลาย', 1),
    Keyword('สวย', 1),
]

KEYWORDS_FUNCTIONAL = [
    Keyword('เพิ่ม', 2),
    Keyword('ลด', 2),
    Keyword('บวก', 2),
    Keyword('ลบ', 2),
    Keyword('ดู', 2),
    Keyword('เปิิด', 2),
    Keyword('ปิด', 2),
    Keyword('เข้า', 2),
    Keyword('ล็อก', 2),
    Keyword('วิเคราะห์', 2),
    Keyword('เลื่อน', 2),
    Keyword('สามารถ', 2),
    Keyword('คำนวณ', 2),
    Keyword('ทำ', 2),
    Keyword('โหลด', 2),
    Keyword('ใส่', 2),
    Keyword('รายการ', 2),
    Keyword('ฟีเจอร์', 2),
    Keyword('ฟังก์ชัน', 2),
]

KEYWORDS_NON_FUNCTIONAL = [
    Keyword('รูป', 3),
    Keyword('ภาพ', 3),
    Keyword('สี', 3),
    Keyword('ลาย', 3),
    Keyword('ฟอนต์', 3),
    Keyword('ตัวหนังสือ', 3),
    Keyword('ตกแต่ง', 2),
]


def get_data_group_by_priority(data):
    list_high = list()
    list_medium = list()
    list_low = list()

    for i in data:
        score = [0, 0, 0]

        score[0] = calculate_score(i, KEYWORDS_HIGH_PRIORITY)
        score[1] = calculate_score(i, KEYWORDS_MEDIUM_PRIORITY)
        score[2] = calculate_score(i, KEYWORDS_LOW_PRIORITY)

        try:
            result = round((score[0] * 0 + score[1] * 1 + score[2] * 2)/sum(score))
        except ZeroDivisionError:
            result = 1

        if result == 0:
            list_high.append(i)
        elif result == 1:
            list_medium.append(i)
        elif result == 2:
            list_low.append(i)

    return list_high, list_medium, list_low


def get_data_group_by_functionality(data):
    list_functional = list()
    list_non_functional = list()

    for i in data:
        score = [0, 0]

        score[0] = calculate_score(i, KEYWORDS_FUNCTIONAL)
        score[1] = calculate_score(i, KEYWORDS_NON_FUNCTIONAL)

        try:
            result = round((score[0] * 2 + score[1] * 1)/sum(score))
        except ZeroDivisionError:
            result = 1

        if result == 2:
            list_functional.append(i)
        elif result == 1:
            list_non_functional.append(i)

    return list_functional, list_non_functional


def get_data_group_by_keyword(data):
    dict_keywords = dict()

    all_data = list()
    counted_data = dict()

    exceptions = [
        'นะ',
        'แอป',
        'แอปพลิเคชัน'
    ]

    # Step 1: Append all received data
    for i in data:
        all_data.append(pos_tag(TOKENIZER.word_tokenize(i.description)))

    # Step 2: Count and clean other word types than NCMN (Probably nouns)
    for i in all_data:
        for j in i:
            if j[1] == 'NCMN' and j[0] not in exceptions:
                if j not in counted_data:
                    counted_data[j] = 1
                else:
                    counted_data[j] += 1

    # Step 3: Remove exceeded keywords
    while len(counted_data) > 9:
        minimum = 2
        for i in sorted(counted_data, key=lambda x: counted_data[x]):
            if counted_data[i] < minimum:
                counted_data.pop(i)
        minimum += 1

    for i in counted_data:
        dict_keywords[i[0]] = [j for j in data if i[0] in TOKENIZER.word_tokenize(j.description)]

    temp = list()
    for i in dict_keywords:
        for j in dict_keywords[i]:
            if j not in temp:
                temp.append(j)

    dict_keywords['อื่น ๆ'] = [i for i in data if i not in temp]

    return dict_keywords


def calculate_score(data, source):
    score = 0

    for i in source:
        check = True
        for j in TOKENIZER.word_tokenize(i.word):
            if j not in TOKENIZER.word_tokenize(data.description):
                check = False
                break
        score += i.weight * check

    return score
