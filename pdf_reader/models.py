from dataclasses import dataclass, field
from typing import List

@dataclass
class Person:
    nit: str = None
    name: str = None
    mother_name: str = None
    cpf: str = None
    born: str = None
    relationships: List['Relationships'] = field(default_factory=list)

    def insert_relationship(self, relationship) -> None:
        self.relationships.append(relationship)

@dataclass
class Relationships:
    seq: int = None
    emp_code: str = None
    bond_origin: str = None
    registered_worker: str = None
    type_affiliated: str = None
    start_date: str = None
    end_date: str = None
    last_remuneration: str = None