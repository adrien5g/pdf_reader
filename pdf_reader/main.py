from read_pdf import Pdf
from pprint import pprint as print

pdf = Pdf()
page = pdf.paginate_pdf()[0]
person = pdf.generate_person_data(pdf.extract_text(page))

all_pages = pdf.paginate_pdf()
text = pdf.merge_text_and_remove_header_and_footer(all_pages)
person = pdf.generate_relationships(person, text)
print(person)