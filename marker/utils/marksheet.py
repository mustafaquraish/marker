import yaml

class Marksheet():
    def __init__(self):
        self.data = {}

    def load(self, marksheet_path):
        '''
        Initialize the marksheet with the contents of a file
        '''
        with open(marksheet_path) as marksheet:
            self.data = yaml.safe_load(marksheet)
    
    def add_students(self, student_list):
        '''
        Add a list students to the marksheet if they don't already exist
        '''
        for student in student_list:
            if student not in self.data:
                self.data[student] = None
    
    def marked_items(self):
        '''
        Return the student: mark_list pairs for all the marked students
        '''
        for student in self.data:
            mark_list = self.data[student] 
            if mark_list is not None:
                yield student, mark_list

    def items(self):
        '''
        Return all student: mark_list pairs
        '''
        return self.data.items()

    def unmarked(self):
        '''
        Generates all the unmarked student names in the marksheet
        '''
        for student, mark in self.data.items():
            if mark is None:
                yield student
    
    def update(self, student, mark_list):
        '''
        Update the marklist for a student
        '''
        self.data[student] = mark_list
    
    def save(self, destination_path):
        '''
        Saves the marksheet to a file.

        NOTE: This is not a robust yaml dump, but it ensures that the output 
              file contains blanks instead of 'null's for unmarked students.
              This conveniently works because yaml supports array notation, 
              and so the mark_lists can be written directly to yaml.
        '''
        with open(destination_path, 'w') as marksheet:
            for student, mark in self.data.items():
                if mark is None:
                    mark = ""
                marksheet.write(f'{student}: {mark}\n')

