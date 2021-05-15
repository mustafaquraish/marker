import yaml

class Marksheet():

    # --------------------------- I/O -----------------------------------------

    def __init__(self, marksheet_path=None):
        '''
        Initialize an empty marksheet or with the contents of a file
        '''
        if marksheet_path is None:
            self.data = {}
        else:
            with open(marksheet_path) as marksheet:
                self.data = yaml.safe_load(marksheet)
            if self.data is None:
                self.data = {}

    def load(self, marksheet_path):
        '''
        Initialize the marksheet with the contents of a file
        '''
        with open(marksheet_path) as marksheet:
            self.data = yaml.safe_load(marksheet)
        if self.data is None:
            self.data = {}

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
                if student is not None:
                    marksheet.write(f'{student}: {mark}\n')
    
    # ----------------------- Marks Bookkeeping -------------------------------


    def add_students(self, student_list):
        '''
        Add a list students to the marksheet if they don't already exist
        '''
        for student in student_list:
            if student not in self.data and student is not None:
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

    def __getitem__(self, student):
        if student not in self.data or self.data[student] is None:
            return []
        return self.data[student]

    def __setitem__(self, student, mark_list):
        self.data[student] = mark_list

    def unmarked_students(self):
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

    # --------------------- Statistics ----------------------------------------

    def get_mark_totals(self, only_compiled=False):
        '''
        Returns an array of (summed) total marks for each marked student.
        Optionally, return marks for only compiled submissions.
        '''
        if only_compiled:
            return [sum(marks) for _, marks in self.marked_items() if marks != []] 
        else:
            return [sum(marks) for _, marks in self.marked_items()]

    def num_marked(self):
        return len(self.get_mark_totals(False))

    def num_compiled(self):
        return len(self.get_mark_totals(True))

    def num_compile_failed(self):
        return self.num_marked() - self.num_compiled()

    def mean(self, only_compiled=False):
        marks_list = self.get_mark_totals(only_compiled)
        return sum(marks_list) / len(marks_list)

    def median(self, only_compiled=False):
        marks_list = self.get_mark_totals(only_compiled)
        return sorted(marks_list)[ len(marks_list) // 2 ]

    def get_distribution(self, only_compiled=False):
        '''
        Return a dictionary containing key value pairs of:
            { <mark> : number of students with <mark> }
        '''
        marks_list = self.get_mark_totals(only_compiled)        
        distribution = {
            i : marks_list.count(i) 
                for i in range(max(marks_list) + 1)
        }
        return distribution
