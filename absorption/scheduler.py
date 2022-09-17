# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:28:13 2022

@author: ilara
"""

class Scheduler:
    def __init__(self, name='default_Scheduler'):
        self.name = name
        # self.ug_priorities = {}
        
    def set_ug_priorities(self, priorities_dict):
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
        
        print('NACHOOO: priorities is: ',priorities)
        ranks = self.assign_ug_priorities(ugs, priorities)    
        for i, student in enumerate(students):
            student.ug_priority = ranks[i]
            
        return sorted(students, key=lambda x: x.ug_priority)
    
    # def prioritize_students(self, students, philosophy='fixed', tiebreaker=None,
    #                         priorities=None):
        
    #     tiebreakers = {'flight_date': self.prioritize_students_by_flight_date}
        
    #     philosophies = {'fixed': lambda x: x,
    #                     'upgrade': self.prioritize_students_by_ug}
        
    #     if tiebreaker is not None:
    #         try:
    #             tie_func = tiebreakers[tiebreaker]
    #         except KeyError:
    #             print('Invalid tiebreaker method.')
    #             return students    
    #         students = tie_func(students)
            
    #     try:
    #         sort_func = philosophies[philosophy]
    #     except KeyError:
    #         print('Invalid prioritization philosophy.')
    #         return students
        
    #     prioritized = sort_func(students, priorities)
        
    #     return prioritized

            
        
        