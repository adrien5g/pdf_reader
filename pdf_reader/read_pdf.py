from typing import Dict, List

from models import Person, Relationships

from PyPDF2 import PdfReader, PageObject

class Pdf:

    def __init__(self) -> None:
        self.reader = PdfReader('data.pdf')
        self.total_pages = len(self.reader.pages)
    
    def paginate_pdf(self) -> List[PageObject]:
        return self.reader.pages
    
    def merge_text_and_remove_header_and_footer(self, text: List[PageObject]) -> str:
        all_text = ''
        for page in text:
            header = []
            data = page.extract_text()

            for line in data.split('\n'):
                if 'Trabalhador' in line:
                    break
                header.append(line)
            header: str = '\n'.join(header)
            all_text += data.replace(header, '')
        skip = True
        footer = []
        for page in text:
            data = page.extract_text()
            for line in data.split('\n'):
                if 'o inss poderá rever a qualquer tempo' in line.lower():
                    skip = False
                if not skip:
                    footer.append(line)
            break
        all_text = all_text.replace('\n'.join(footer), '')
        return all_text

    def extract_text(self, page: PageObject) -> str:
        text = page.extract_text()
        return text

    def generate_person_data(self, text: str) -> Person:
        lines = text.split('\n')

        row_4_splitted = lines[4].split(':')
        nit = row_4_splitted[1].split(' ')[1].strip()
        cpf = row_4_splitted[2].split(' ')[1].strip()
        name = row_4_splitted[-1]

        row_5_splitted = lines[5].split(':')
        born = row_5_splitted[1].split(' ')[1].strip()
        mother = row_5_splitted[-1].strip()
        pag_index = mother.index('Página')
        mother = mother[:pag_index]

        person = Person(nit, name, mother, cpf, born)
        return person
    
    def generate_relationships(self, person: Person, text: str) -> Person:
        relationships: Dict[int, List[str]] = {}
        current_relatioship = 0
        start = False
        for line_text in text.split('\n'):
            if line_text.strip() == 'Trabalhador':
                current_relatioship += 1
                start = True
                continue
            elif line_text.strip().startswith('O INSS'):
                break
            elif start:
                if not current_relatioship in relationships.keys():
                    relationships[current_relatioship] = []
                relationships[current_relatioship].append(line_text)
        
        for relationship in relationships.values():
            rel = self.gen_relantionship(relationship)
            person.insert_relationship(rel)
        return person

    def gen_relantionship(self, text: List[str]) -> Relationships:
        seq = self.__get_seq(text)
        emp_code = self.__get_emp_code(text)
        bond_origin = self.__get_bond_origin(text)
        type_affiliated = self.__get_type_affiliated(text)
        
        relationship = Relationships(seq, emp_code, bond_origin)
        return relationship

    def __get_seq(self, text: List[str]) -> str:
        seq = text[0].split(' ')[0]
        return seq
    
    def __get_emp_code(self, text: List[str]) -> str:
        temp_emp_code = text[0].split(' ')[1]
        emp_code = []
        for i, l in enumerate(temp_emp_code):
            if l.isupper() and i != 0:
                break
            emp_code.append(l)
        emp_code = ''.join(emp_code)
        return emp_code
    
    def __get_bond_origin(self, text: List[str]) -> str:
        temp_bond_origin: List[str] = []
        first_upper = False
        new_text = ''.join(text)
        text: str = new_text.replace('Indeterminado', '').replace('Empregado', '')
        for letter in text:
            if letter.isupper():
                first_upper = True
            elif first_upper and letter != ' ':
                break
            elif letter.isnumeric() or letter in './-':
                continue
            temp_bond_origin.append(letter)
        bond_origin = ''.join(temp_bond_origin).strip()
        return bond_origin

    def __get_type_affiliated(self, text: List[str]) -> str:
        # print(text)
        ...