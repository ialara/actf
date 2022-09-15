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

if __name__ == '__main__':
    pytest.main()