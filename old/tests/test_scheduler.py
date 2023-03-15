# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:24:24 2022

@author: ilara
"""

import pytest
from context import absorption
from absorption import scheduler

class MockStudent:
    def __init__(self, i, last_flight_day, ug, ride_num=None):
        self.id = i
        self.last_flight_day = last_flight_day
        self.ug = ug
        self.ride_num = ride_num
        
    def get_last_flight(self):
        return self.last_flight_day
    
    def get_upgrade(self):
        return self.ug
    
    def get_next_ug_ride(self):
        return self.ride_num
    
class MockIP:
    def __init__(self, i, sorties=200):
        self.id = i
        
class MockSyllabus:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        
    def specify_support_pilot_resources(self, fls, wgs):
        assert len(fls) == len(wgs) == self.duration, 'Lengths mismatch'
        resources = []
        for ride in range(self.duration):
            resources.append({'IP': 1,
                            'FL': fls[ride],
                            'WG': wgs[ride]})
        self.support_pilot_resources = resources   
        
    def get_support_pilot_resources_for_ride(self, ride):
        return self.support_pilot_resources[ride]
        
        
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
        students.append(MockStudent(i, day, ugs[i], i))
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

@pytest.fixture
def my_MQT():
    syll = MockSyllabus('MQT', 9)
    fls = [0, 0, 0, 0, 1, 3, 0, 2, 3]
    wgs = [0, 0, 0, 0, 1, 3, 0, 2, 3]
    
    syll.specify_support_pilot_resources(fls, wgs)
    return syll

@pytest.fixture
def my_FLUG():
    syll = MockSyllabus('FLUG', 8)
    fls = [0, 0, 0, 1, 3, 0, 2, 3]
    wgs = [0, 0, 0, 1, 3, 0, 2, 3]
    
    syll.specify_support_pilot_resources(fls, wgs)
    return syll

@pytest.fixture
def my_IPUG():
    syll = MockSyllabus('IPUG', 8)
    fls = [0, 0, 0, 1, 3, 0, 2, 3]
    wgs = [0, 0, 0, 1, 3, 0, 2, 3]
    
    syll.specify_support_pilot_resources(fls, wgs)
    return syll

@pytest.fixture
def my_syllabi(my_MQT, my_FLUG, my_IPUG):
    return {'MQT': my_MQT, 'FLUG': my_FLUG, 'IPUG': my_IPUG}
    
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
    
def test_specify_ug_priorities(my_scheduler, ug_priorities):
    my_scheduler.specify_ug_priorities(ug_priorities)
    assert my_scheduler.ug_priorities == ug_priorities
    
def test_determine_student_sortie_support_reqs(my_scheduler, my_students, my_syllabi):
    ## Expected
    # IPUG Ride 0: IP: 1, FL: 0, WG: 0
    # IPUG Ride 1: IP: 1, FL: 0, WG: 0
    # FLUG Ride 2: IP: 1, FL: 0, WG: 0
    #  MQT Ride 3: IP: 1, FL: 0, WG: 0
    # FLUG Ride 4: IP: 1, FL: 3, WG: 3
    #  MQT Ride 5: IP: 1, FL: 3, WG: 3
    #  MQT Ride 6: IP: 1, FL: 0, WG: 0
    # FLUG Ride 7: IP: 1, FL: 3, WG: 3
    expected = [{'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 3, 'WG': 3},
                {'IP': 1, 'FL': 3, 'WG': 3},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 3, 'WG': 3}]
    actual_students = my_scheduler.determine_student_sortie_support_reqs(my_students, my_syllabi)
    assert [s.next_ug_sortie_support_reqs for s in actual_students] == expected
    
def test_allocate_ug_sorties_within_daily_sortie_limit(my_scheduler, my_students):
    # Assumes students have already been prioritized; this test just checks limiting logic.
    sortie_limit = 14 #e.g, 8 turn 6
    # Notional, do not align with student syllabi specified in my_students.
    support_reqs = [{'IP': 1, 'FL': 0, 'WG': 0}, # Student 0 (1+student = 2 sorties)
                    {'IP': 1, 'FL': 3, 'WG': 3}, # Student 1 (8 sorties)
                    {'IP': 1, 'FL': 0, 'WG': 0}, # Student 2 (2 sorties)
                    ## == Should stop here (12 sorties) because cannot fly next chunk ==
                    {'IP': 1, 'FL': 2, 'WG': 2}, # Student 3 (6 sorties)
                    {'IP': 1, 'FL': 3, 'WG': 3}, # Student 4 (8 sorties)
                    {'IP': 1, 'FL': 0, 'WG': 0}] # Student 5 (2 sorties)
    
    for i in range(len(support_reqs)):
        my_students[i].next_ug_sortie_support_reqs = support_reqs[i]
        
    expected_students_scheduled = [0, 1, 2]
    expected_sorties_scheduled = 12
    
    actual_students = my_scheduler.allocate_ug_sorties(my_students, sortie_limit)
    actual_sorties = len(actual_students) + sum([sum(s.next_ug_sortie_support_reqs.values()) for s in actual_students])
    assert [s.id for s in actual_students] == expected_students_scheduled
    assert actual_sorties == expected_sorties_scheduled
    assert actual_sorties <= sortie_limit
    
    
        
    
    

@pytest.mark.xfail # Not Implemented   
def test_determine_daily_ug_support_pilot_requirements(my_scheduler, my_students):
    expected = 46
    students = my_students
    support = support_pilots
    actual = my_scheduler.determine_daily_ug_support_reqs(students, support)
    assert actual == expected

# if __name__ == '__main__':
#     pytest.main(["-v"])