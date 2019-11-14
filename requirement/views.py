from django.shortcuts import render

from requirement.analysis import RequirementData


def index(request):
    ''' View Method: Index '''
    context = dict()

    if request.method == 'POST':
        title = request.POST.get('title')
        requirements = request.POST.get('requirements')

        context['data'] = RequirementData(title, requirements)

    context['data'] = RequirementData('แอปยา', [
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
    ])

    return render(request, template_name='requirement/index.html', context=context)
