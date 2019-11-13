'''
    analyze.py
    https://www.thainlp.org/pythainlp/tutorials/notebooks/pythainlp-get-started.html
'''

from pythainlp import word_tokenize
from pythainlp.tag import pos_tag


class Keyword():
    '''
        Class: Keyword
        Purpose: Contains data of keyword
    '''
    def __init__(self, word, weight):
        self.word = word     # Type: String
        self.weight = weight # Type: Integer


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

def main():
    data = [
        'แอปต้องดูรายการยาได้',
        'แอปต้องเพิ่มยาได้',
        'ต้องล็อกอินได้',
        'ต้องดูเวลาทานยาได้',
        'ต้องดูรายการหมอได้',
        'ต้องดูแผนที่โรงพยาบาลได้',
        'ล็อกอินแล้วข้อมูลไม่หาย',
        'ล็อกอินแล้วค้างไว้ได้',
        'ไม่ทำให้ผู้ใช้หงุดหงิด',
        'คลิกรายการโรงพยาบาลแล้วไปที่แผนที่ทันที',
        'รองรับกลุ่มผู้ใช้ที่ตาบอดสี',
        'ถ้าเป็นฟอนต์ใหญ่ก็ดี',
        'ไอคอนเอาไรก็ได้',
        'ไม่เอารูปแมงมุมในแอปเด็ดขาด',
        'ใส่รูปแมงมุมมาด่านะ',
        'ใส่รูปแมงมุมมาลูกค้าไม่เอานะ',
        'อยากได้สีฟ้า',
        'อยากให้แอปมีรูปไดโนเสาร์ร้องเพลง แต่ถ้าไม่มีไม่เป็นไร',
        'ลายก้อนเมฆก็สวยนะ',
        'ใส่รูปหมาชิบะก็น่ารักนะ',
        'อยากให้เป็นแอปที่ใช้ได้ทุกคน',
        'ผู้ใช้ต้องไม่พบปัญหาโหลดนาน',
        'เลื่อนขึ้นเลื่อนลงได้',
    ]

    get_data_group_by_priority(data)
    get_data_group_by_functionality(data)
    get_data_group_by_keyword(data)


def get_data_group_related(data):
    # TODO: Implements function
    pass


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

    # print_result({
    #     'HIGH': list_high,
    #     'MEDIUM': list_medium,
    #     'LOW': list_low
    # })

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

    # print_result({
    #     'FUNCTIONAL': list_functional,
    #     'NON-FUNCTIONAL': list_non_functional,
    # })

    return list_functional, list_non_functional


def get_data_group_by_keyword(data):
    all_data = list()

    for i in data:
        all_data.append(pos_tag(word_tokenize(i)))

    for i in all_data:
        for j in i:
            if j[1] == 'NCMN':
                print(j)

    return


def calculate_score(data, source):
    score = 0

    for j in source:
        check = True
        for k in word_tokenize(j.word, keep_whitespace=False):
            if k not in word_tokenize(data, keep_whitespace=False):
                check = False
                break
        score += j.weight * check

    return score


def print_result(data):
    for i in data:
        print('\n- {} -'.format(i))
        _ = [print(j) for j in data[i]]
    print()

main()
