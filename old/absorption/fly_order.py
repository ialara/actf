# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:16:02 2022

@author: ilara
"""

class FlySchedule:
  ug_priorities = {'MQT': 1,
                   'IPUG': 2,
                   'FLUG': 3}

  scheduling_philosophy = 'progression'

  max_fhp = 80
  max_wss = 68

  def __init__(self, students, instructors, support, gos=3, name='default_FlySchedule'):
    self.name = name
    self.ups = students
    self.ips = instructors
    self.spt = support
    self.gos = gos

  def assign_student_priorities(self, students):
    for id, student in students.items():
      student['priority'] = FlySchedule.ug_priorities[student.return_upgrade()]

  def make_schedule(self):
    scheduled_lines = []
    ips = {}
    ups = {}
    spt = {}

    for _ in range(self.gos):
      available_students = list(self.ups)
      if self.ug_sortie_possible(self.ips, self.ups, self.spt):
        ip = self.ips[rng.choice(list(self.ips))]
        up = self.ups[rng.choice(available_students)]
        available_students.remove(up.id) # Student can't fly twice on same day
        num_spt = 2
      else:
        num_spt = 4 # CT
      
      if len(self.spt) >= num_spt:
        spt_ids = rng.choice(list(self.spt), num_spt, replace=False)
        spt = [self.spt[id] for id in spt_ids]
      
      scheduled_lines.append(FlightCrew(ips, ups, spt))
      return scheduled_lines    

  def ug_sortie_possible(self, ips, students, support):
    return len(ips) > 0 and len(students) > 0 and len(support) >= 2  