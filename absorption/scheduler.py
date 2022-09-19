# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:28:13 2022

@author: ilara
"""

class Scheduler:
    def __init__(self, name='default_Scheduler'):
        self.name = name
        # self.ug_priorities = {}
        
    def specify_ug_priorities(self, priorities_dict):
        self.ug_priorities = priorities_dict
        
    def prioritize_students_by_flight_date(self, students):
        return sorted(students, key=lambda x: x.get_last_flight())
    
    def assign_ug_priorities(self, upgrades, priorities):
        return [priorities[ug] for ug in upgrades]
    
    def prioritize_students_by_ug(self, students, priorities=None):
        ugs = [s.get_upgrade() for s in students]
        if priorities is None:
            try:
                priorities = self.ug_priorities
            except AttributeError:
                print('''
                      Attempting to use upgrade priorities, but none provided.
                      Either pass priorities as argument, or call set_ug_priorities().
                      ''')
                return students

        ranks = self.assign_ug_priorities(ugs, priorities)    
        for i, student in enumerate(students):
            student.ug_priority = ranks[i]
            
        return sorted(students, key=lambda x: x.ug_priority)
    
    def prioritize_students_by_ug_then_date(self, students, priorities=None):
        inner_sort = self.prioritize_students_by_flight_date(students)
        prioritized = self.prioritize_students_by_ug(inner_sort, priorities)
        return prioritized

    def determine_student_sortie_support_reqs(self, students, syllabi):
        for s in students:
            syllabus = syllabi[s.get_upgrade()]
            ride = s.get_next_ug_ride()
            s.next_ug_sortie_support_reqs = syllabus.get_support_pilot_resources_for_ride(ride)
            
        return students
    
    def allocate_ug_sorties(self, students, sortie_limit):
        sorties_remaining = sortie_limit
        scheduled_students = []
        students_iter = iter(students)
        
        next_stud = next(students_iter)
        sum_support_reqs = sum(next_stud.next_ug_sortie_support_reqs.values())
        while sorties_remaining > sum_support_reqs - 1:
            scheduled_students.append(next_stud)
            sorties_remaining -= sum_support_reqs + 1
            try: 
                next_stud = next(students_iter)
                sum_support_reqs = sum(next_stud.next_ug_sortie_support_reqs.values())
            except StopIteration:
                break
        
        return scheduled_students
        
            
        
            
        
        