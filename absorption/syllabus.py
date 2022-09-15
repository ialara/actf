# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:16:27 2022

@author: ilara
"""

class Syllabus:
    def __init__(self, name, duration, ending_award):
        self.name = name
        self.duration = duration
        self.ending_award = ending_award
    
    def print_(self):
        print(f'{self.name}: {self.duration} rides to earn {self.ending_award}')
        
class ExperiencedBadge:   
    @staticmethod
    def is_experienced(pilot):
        return pilot.get_sorties() >= 250 and 'FL' in pilot.get_quals()