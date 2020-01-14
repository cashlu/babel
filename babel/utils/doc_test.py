from docx import Document


# document = Document('../../base_docs/test.docx')
#
# for para in document.paragraphs:
#     for run in para.runs:
#         run.text = run.text.replace('A03', '替换A03')
#
# for table in document.tables:
#     for row in table.rows:
#         for cell in row.cells:
#             if cell.text == 'A05':
#                 cell.text = cell.text.replace('A05', '替换A05')
#                 print('替换一次')
#
# document.save('../../base_docs/dest.docx')


# TODO: 重写方法，初步的想法是将要替换的所有代号和具体内容存进一个dict中，然后遍历文档，
#  如果文档中包含dict的key中的代号，则替换文本。
def replace_content(document, old_str, new_str):
    for para in document.paragraphs:
        for run in para.runs:
            run.text = run.text.replace(old_str, new_str)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text == old_str:
                    cell.text = cell.text.replace(old_str, new_str)
                    print('替换一次')
    document.save('../../base_docs/dest.docx')


if __name__ == '__main__':
    doc = Document('../../base_docs/test.docx')
    replace_content(doc, 'A05', '替换测试')
