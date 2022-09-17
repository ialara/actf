# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:24:24 2022

@author: ilara
"""

import pytest
from context import absorption
from absorption import scheduler

class MockStudent:
    def __init__(self, i, last_flight_day, ug):
        self.id = i
        self.last_flight_day = last_flight_day
        self.ug = ug
        
    def get_last_flight(self):
        return self.last_flight_day
    
    def get_upgrade(self):
        return self.ug
    
class MockIP:
    def __init__(self, i, sorties=200):
        self.id = i
        
        
days = [1,     10,     3,     4,      2,     9,    9,      2]
ugs = ['IPUG','IPUG', 'FLUG', 'MQT', 'FLUG', 'MQT', 'MQT', 'FLUG']
days_sorted = sorted(days)

## expected for MQT>IPUG>FLUG priorities and given days/ugs:
# [('MQT', 4) <- [3],
#  ('MQT', 9) <- [5],
#  ('MQT', 9) <- [6],
#  ('IPUG', 1) <- [0],
#  ('IPUG', 10) <- [1],
#  ('FLUG', 2) <- [4],
#  ('FLUG', 2) <- [7],
#  ('FLUG', 3) <- [2]
## so UG-date priority of pilot id should be: [3, 5, 6, 0, 1, 4, 7, 2]

@pytest.fixture
def my_students():
    students = []
    for i, day in enumerate(days):
        students.append(MockStudent(i, day, ugs[i]))
    return students

@pytest.fixture
def my_scheduler():      
    sched = scheduler.Scheduler(name='test_Scheduler')
    return sched

@pytest.fixture
def ug_priorities():
    my_priorities = {'MQT': 1,
                  'IPUG': 2,
                  'FLUG': 3}
    return my_priorities
    
def test_students_prioritized_by_last_flight_date(my_students, my_scheduler):
    prioritized = my_scheduler.prioritize_students_by_flight_date(my_students)
    actual = [student.get_last_flight() for student in prioritized]
    assert actual == days_sorted
    
def test_upgrades_assigned_scheduling_priority(my_students, my_scheduler, ug_priorities):
    expected = [ug_priorities[x] for x in ugs]
    student_ugs = [s.get_upgrade() for s in my_students]
    actual = my_scheduler.assign_ug_priorities(student_ugs, ug_priorities)
    assert actual == expected
    
def test_students_prioritized_by_ug(my_students, my_scheduler, ug_priorities):
    expected_ids = [3, 5, 6, 0, 1, 2, 4, 7] # Matches within UG are left in order they were passed
    prioritized = my_scheduler.prioritize_students_by_ug(my_students, ug_priorities)
    actual_ids = [student.id for student in prioritized]
    assert actual_ids == expected_ids
    
def test_scheduling_philosophy_ug_then_date(my_students, my_scheduler, ug_priorities):
    expected_ids = [3, 5, 6, 0, 1, 4, 7, 2] # See above. Matches with same ug/date are left in order passed
    # 
    prioritized = my_scheduler.prioritize_students_by_ug_then_date(my_students, ug_priorities)
    actual_ids = [student.id for student in prioritized]
    assert actual_ids == expected_ids
    
def test_set_ug_priorities(my_scheduler, ug_priorities):
    my_scheduler.set_ug_priorities(ug_priorities)
    assert my_scheduler.ug_priorities == ug_priorities
    
def test_determine_daily_ug_support_pilot_requirements(my_scheduler, my_students):
    expected = 46
    students = my_students
    support = support_pilots
    actual = my_scheduler.determine_daily_ug_support_reqs(students, support)
    assert actual == expected

if __name__ == '__main__':
    pytest.main(["-v"])