# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 14:33:58 2022

@author: ilara
"""

import pytest
from context import absorption
from absorption import syllabus

# Arrange
## EXP Definition (business rules)
exp_sorties = 250
exp_quals = 'FL'

class MockPilot:
    def __init__(self, sorties, quals):
        self.sorties = sorties
        self.quals = quals
        
    def get_sorties(self):
        return self.sorties
    
    def get_quals(self):
        return self.quals

@pytest.fixture
def my_syllabus():
    # In this notional example, assume:
    # All Rides have 1 IP, 1 Student
    # Ride 0: 2-ship (0 FL, 0 WG)
    # Ride 1: 2-ship (0 FL, 0 WG)
    # Ride 2: 4-ship (1 FL, 1 WG)
    # Ride 3: 4v4    (3 FL, 3 WG)
    # Ride 4: 2v4    (2 FL, 2 WG)    
    return syllabus.Syllabus('test', 5, 'testAward')

def test_pilot_meeting_all_requirements_is_experienced():
    mock_pilot = MockPilot(exp_sorties, [exp_quals])
    assert syllabus.ExperiencedBadge.is_experienced(mock_pilot)
    
def test_pilot_meeting_only_sorties_is_not_experienced():
    mock_pilot = MockPilot(exp_sorties, [])
    assert not syllabus.ExperiencedBadge.is_experienced(mock_pilot)
    
def test_pilot_meeting_only_quals_is_not_experienced():
    mock_pilot = MockPilot(exp_sorties-1, [exp_quals])
    assert not syllabus.ExperiencedBadge.is_experienced(mock_pilot)
    
def test_pilot_meeting_no_requirements_is_not_experienced():
    mock_pilot = MockPilot(exp_sorties-1, [])
    assert not syllabus.ExperiencedBadge.is_experienced(mock_pilot)
    
def test_specify_support_pilot_resources(my_syllabus):
    expected = [{'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 1, 'WG': 1},
                {'IP': 1, 'FL': 3, 'WG': 3},
                {'IP': 1, 'FL': 2, 'WG': 2}]
    fl_requirements = [0, 0, 1, 3, 2]
    wg_requirements = [0, 0, 1, 3, 2]
    
    my_syllabus.specify_support_pilot_resources(fls=fl_requirements, wgs=wg_requirements)
    assert my_syllabus.support_pilot_resources == expected
    
def test_get_support_pilot_resources_for_ride(my_syllabus):
    expected = [{'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 1, 'WG': 1},
                {'IP': 1, 'FL': 3, 'WG': 3},
                {'IP': 1, 'FL': 2, 'WG': 2}]
    my_syllabus.support_pilot_resources = expected
    
    assert my_syllabus.get_support_pilot_resources_for_ride(3) == expected[3]
    assert my_syllabus.get_support_pilot_resources_for_ride(0) == expected[0]
    assert my_syllabus.get_support_pilot_resources_for_ride(4) == expected[4]
    
def test_get_support_resources_with_bad_ride_num_raises_IndexError(my_syllabus):
    expected = [{'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 0, 'WG': 0},
                {'IP': 1, 'FL': 1, 'WG': 1},
                {'IP': 1, 'FL': 3, 'WG': 3},
                {'IP': 1, 'FL': 2, 'WG': 2}]
    my_syllabus.support_pilot_resources = expected
    with pytest.raises(IndexError):
        my_syllabus.get_support_pilot_resources_for_ride(5)  

# if __name__ == '__main__':
#     pytest.main()