from dataclasses import dataclass


class InvalidStudentError(Exception):
    """Raised when student data is invalid."""
    pass


@dataclass(frozen=True)
class Student:
    id: str
    matricule: str
    name: str
    #Represents a student within the academic domain.
    #The frozen=True parameter makes the object immutable once created:
    # no attribute can be modified after the instance is constructed.
    # This choice reflects a defensive design principle — a Student
    # should not be silently alterable by another part of the system,
    # which guarantees data consistency throughout the object's
    #lifecycle. "
   
    def __post_init__(self):
        #Validates business invariants immediately after object
       # creation."

        #rules 1: a student must have an identifier,the id is used as the identity key.
        if not self.id:
            raise InvalidStudentError("Id cannot be empty.")
        #rules 2: the matricule is the student's officiel institutional
        #identifier, it cannot be empty
        if not self.matricule:
            raise InvalidStudentError("Matricule cannot be empty.")
        #rules 3: an empty name carries no semantic meaning for representing a real
        #person within this domain
        if not self.name:
            raise InvalidStudentError("Name cannot be empty.")

    def full_name(self) -> str:
        return self.name
        #return the student's full name

    def has_matricule(self, matricule: str) -> bool:
        return self.matricule == matricule
        #checks wheter the given matricule matches the student's matricule

etudiant = Student(id="202504039", matricule="MAT141", name="kenson janvier")

print(etudiant.full_name())            # Jean Pierre
print(etudiant.has_matricule("MAT141")) # True
print(etudiant.has_matricule("XXX"))    # False