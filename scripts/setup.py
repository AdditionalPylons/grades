import argparse
import csv

from datetime import date, timedelta
from random import choice, randrange

class GradeDataWriter:
    """
    Class used to write semi-random grade data
    for a given school subject.
    """

    students = [
            "Bill Edwards",
            "David Chen",
            "William Chen",
            "Rafferty Russell",
            "Jason Ramirez",
            "Fred Fernando",
            "杨作亮 AlexYang",
            ]

    _class_assignment_mappings = {
        "math": [
            "Plot your address on a coordinate plane",
            "Normalize a data set of your choosing",
            "Calculate the area under a bell curve",
            ],
        "chemistry": [
            "ATMC NMBRS",
            "PLYMER & ALDEHYDE",
            "ELECTRON CONFIG",
            ],
        "spanish": [
            "¡Hola! ¿Cómo se llama?",
            "¿A dónde vamos hoy?",
            "Describe a tu familia",
            "Verbos importantes: ser, estar, haber"
            ]
        }

    def __init__(self, subject: str, num_rows: int, num_makeups: int):
        
        self.subject = subject
        self.num_rows = num_rows
        self.num_makeups = num_makeups
        self.assignment_descriptions = self._class_assignment_mappings.get(self.subject)
        
    def _build_rows(self) -> list[dict]:
        """
        Build and return all rows for writing to the CSV.
        """

        rows = []
        student_idx = 0
        assignment_no = 1
        student_gpa_floors = {student: choice([90, 80, 70, 60, 0]) for student in self.students}
        start_date = date(2022, 1, 1)
        num_makeups = self.num_makeups
        
        for _ in range(self.num_rows):

            if assignment_no - 1 < len(self.assignment_descriptions):
                current_student = self.students[student_idx]
                gpa_floor = student_gpa_floors[current_student]
                date_due = start_date + timedelta(days=choice([0, 365]))
                date_submit = date_due + timedelta(days=(choice([0, 14])))

                rows.append(
                    {
                    "FIRST": current_student.split(" ")[0],
                    "LAST": current_student.split(" ")[1],
                    "SUBJECT": self.subject,
                    "ASSIGNMENT_NO": assignment_no,
                    "ASSIGNMENT_DESC": self.assignment_descriptions[assignment_no - 1],
                    "GRADE": randrange(gpa_floor, gpa_floor + 10) if gpa_floor != 0 else randrange(gpa_floor, gpa_floor + 60),
                    "MAKEUP": False,
                    "DATE_DUE": date_due,
                    "DATE_SUBMIT": date_submit,
                    }
                )

                if num_makeups > 0:
                    rows.append(
                        {
                        "FIRST": current_student.split(" ")[0],
                        "LAST": current_student.split(" ")[1],
                        "SUBJECT": self.subject,
                        "ASSIGNMENT_NO": assignment_no,
                        "ASSIGNMENT_DESC": self.assignment_descriptions[assignment_no - 1],
                        "GRADE": randrange(gpa_floor, gpa_floor + 10) if gpa_floor != 0 else randrange(gpa_floor, gpa_floor + 60),
                        "MAKEUP": True,
                        "DATE_DUE": date_due,
                        "DATE_SUBMIT": date_submit + timedelta(days=(choice([1, 14]))),
                        }
                    )

                    num_makeups -= 1

            else:
                # Log warning but don't raise error, we don't want this to fail for something so trivial
                print("WARNING: More rows of data requested than possible student / assignment combinations!")
                break

            student_idx += 1

            if student_idx >= len(self.students):
                student_idx = 0
                assignment_no += 1

        return rows

    
    def write_rows(self):
        """
        Write all rows to the relevant CSV files.
        """
        rows = self._build_rows()

        with open(f"{self.subject}.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(),delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONE)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject", type=str)
    parser.add_argument("-r", "--rows", type=int, default=100)
    parser.add_argument("-m", "--makeups", type=int, default=0)

    args = parser.parse_args()

    if args.subject:
        GradeDataWriter(args.subject, args.rows, args.makeups).write_rows()
    else:
        for subject in ["math", "chemistry", "spanish"]:
            GradeDataWriter(subject, args.rows, args.makeups).write_rows()