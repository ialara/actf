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
        
        
class ExperiencedBadge:   
    @staticmethod
    def is_experienced(pilot):
        return pilot.get_sorties() >= 250 and 'FL' in pilot.get_quals()