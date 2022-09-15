# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:15:42 2022

@author: ilara
"""

class FlightCrew:
  def __init__(self, ips={}, ups={}, spt={}):
    labels = ['IP', 'UP', 'Support']
    self.crew = {lab: None for lab in labels}

    for duty_position, pilots in zip(labels,[ips, ups, spt]):
      print(pilots)
      if len(pilots) > 0:
        self.crew[duty_position] = pilots

  def summarize(self):
    return {duty: [p.id for p in pilot] for duty, pilot in self.crew.items() if pilot is not None}