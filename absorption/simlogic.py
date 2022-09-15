# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:28:21 2022

@author: ilara
"""

class SimMonth:
  month_num = 0
  def __init__(self, roster):
    self.month = SimMonth.month_num
    self.roster = roster

  def advance(self, months=1):
    SimMonth.month_num += 1
    print(f'=====Month {SimMonth.month_num}====')
    self.update_tos_values(self.roster.pilots, months)
    self.do_inflows(self.roster)
    self.do_outflows(self.roster)
    for _ in range(20):
      self.fly_day(self.roster)

  def update_tos_values(self, pilots, months):
    for id, pilot in pilots.items():
      pilot.increment_tos(months)

  def do_inflows(self, roster):
    self.roster.inflow_nth_tour(num_API1=10, prop_API1_IP=.4, prop_WG=.2, 
                                num_API6=3, prop_API6_IP=.6)
    self.roster.inflow_first_tour(8)

  def do_outflows(self, roster):
    self.roster.outflow_pilots()

  def fly_day(self, roster):
    print('---New day---')
    ips = roster.get_pilots_qualified_as('IP')
    ups = roster.get_students_in('MQT')
    spt = roster.get_pilots_qualified_as('FL')
    sched = FlySchedule(ups, ips, spt)
    lines = sched.make_schedule()
    for line in lines:
      print(line.summarize())
      self.update_instr_sorties(line.crew['IP'])
      self.update_ug_sorties(line.crew['UP'])
      self.update_spt_sorties(line.crew['Support'])

  def update_instr_sorties(self, ip):
    if ip is not None:
      ip.fly_sortie()

  def update_ug_sorties(self, up):
    if up is not None:
      up.fly_ug_sortie()

  def update_spt_sorties(self, spt):
    if spt is not None:
      for pilot in spt:
        pilot.fly_sortie()