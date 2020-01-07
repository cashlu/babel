from docx import Document

document = Document('../../base_docs/test.docx')

for para in document.paragraphs:
    for run in para.runs:
        run.text = run.text.replace('A03', '替换A03')

for table in document.tables:
    for row in table.rows:
        for cell in row.cells:
            if cell.text == 'A05':
                cell.text = cell.text.replace('A05', '替换A05')
                print('替换一次')

document.save('../../base_docs/dest.docx')

# import datetime
#
# now = datetime.datetime.now()
# date = datetime.datetime(2020, 2, 2)
# interval = date - now
# print(interval.days)
