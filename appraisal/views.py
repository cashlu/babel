from django.shortcuts import render


from appraisal.utils import doc_test


def test(request):
    if request.method == 'GET':
        reg_dict = doc_test.dict_generator(1)
        print(reg_dict)
        doc_test.files_generator(reg_dict)
        return render(request, 'appraisal/success.html', {})



