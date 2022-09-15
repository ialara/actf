# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:15:19 2022

@author: ilara
"""
from pilot import Pilot

class SquadronRoster:
    """A collection of Air Force pilots in the same squadron"""
    
    def __init__(self, sq_name, pilots={}):
        self.sq_name = sq_name
        self.pilots = dict(pilots)
        self.pid = 0

    def log(self, msg, prefix='=='):
        print(f'{prefix} {self.sq_name} {msg}')

    def add_INX_pilot(self, f16_sorties=0, tos=0, quals=[], ug=None):
        pid = self.next_pid()
        self.pilots[pid] = Pilot(pid, f16_sorties, tos, api_category=1, quals=quals, ug=ug)
        return self.pilots[pid]

    def next_pid(self):
        if len(self.pilots) > 0:
          self.pid = max(self.pid, max(self.pilots)) + 1
        return self.pid

    def add_EXP_pilot(self, f16_sorties=250, tos=20, api_category=1, quals=ug_quals[:-1], ug=None):
        pid = self.next_pid()
        self.pilots[pid] = Pilot(pid, f16_sorties, tos, api_category, quals, ug)
        return self.pilots[pid]

    def add_pilots(self, new_pilots):
        assert all(isinstance(p, Pilot) for p in new_pilots.values()), 'List must contain Pilot elements'
        self.pilots = self.pilots | new_pilots
        new_pids = new_pilots.keys()
        self.log(f'added PIDs {new_pids}')
        return new_pilots

    def remove_pilots(self, pids):
        assert all(pid in self.pilots for pid in pids), 'Pilot not found'
        self.log(f'removed PIDs {pids}', prefix='..')
        return [self.pilots.pop(pid) for pid in pids] 

    def populate(self, num_API1=26, prop_EXP=0.45, prop_IP=0.4, num_API6=10):
        num_EXP = rng.binomial(num_API1, prop_EXP)
        num_INX = num_API1 - num_EXP
        ip_billets_remaining = rng.binomial(num_EXP, prop_IP)
        staff_billets_remaining = num_API6

        # Parameters
        max_TOS_INX = 24
        min_TOS_EXP = 24
        max_TOS_EXP = 32

        min_f16_sorties_EXP = Pilot.exp_sorties
        max_f16_sorties_EXP = 500

        max_f16_sorties_INX = Pilot.exp_sorties

        staff_billets_remaining = num_API6
        # Add EXP pilots
        for _ in range(num_EXP + num_API6):
            tos = rng.integers(min_TOS_EXP, max_TOS_EXP + 1)
            # Award sorties proportional to TOS
            sorties = int((tos - min_TOS_EXP)/(max_TOS_EXP - min_TOS_EXP) *
                      (max_f16_sorties_EXP - min_f16_sorties_EXP)) + min_f16_sorties_EXP

            quals = ug_quals[:-1] # Assumed that all EXP are at least FL

            if staff_billets_remaining > 0:
                api = 6 # Assign staff first
                staff_billets_remaining -= 1
            else:
                api = 1
                # Assume only API-1 arrive as IP
                if ip_billets_remaining > 0:
                    quals.append(ug_quals[-1])
                    ip_billets_remaining -= 1
              
            self.add_EXP_pilot(sorties, tos, api, quals)

        # Add INX pilots
        for _ in range(num_INX):
            tos = rng.integers(max_TOS_INX + 1)
            sorties = int(tos/max_TOS_INX * max_f16_sorties_INX)

            quals = []

            pilot = self.add_INX_pilot(sorties, tos, quals=[])

            if pilot.tos > 2:
              pilot.award_qual(ug_quals[0])

            else:
              mqt_progress = rng.integers(pilot.syllabi_rides[ug_names[0]]) # Intentionally capping starting INX at 1 MQT ride from end
              pilot.enroll_upgrade(ug_names[0])
              for s in range(mqt_progress):
                pilot.fly_ug_sortie()

    def inflow_nth_tour(self, num_API1, prop_API1_IP, prop_WG, num_API6, prop_API6_IP):
      num_IP = rng.binomial(num_API1, prop_API1_IP)
      num_INX = rng.binomial(num_API1, prop_WG)
      print(f'IP: {num_IP} | INX: {num_INX}')
      num_FL = num_API1 - num_IP - num_INX

      min_sorties_INX = int(0.6*Pilot.exp_sorties)
      max_sorties_INX = int(1.1*Pilot.exp_sorties)

      min_sorties_FL = Pilot.exp_sorties
      max_sorties_FL = int(2.5*Pilot.exp_sorties)

      min_sorties_IP = int(1.5*Pilot.exp_sorties)
      max_sorties_IP = 5*Pilot.exp_sorties

      new_nth_pilots = []

      for _ in range(num_INX):
        sorties = rng.integers(min_sorties_INX, max_sorties_INX)
        pilot = self.add_INX_pilot(f16_sorties=sorties, quals=[ug_quals[0]])
        new_nth_pilots.append(pilot)

      for _ in range(num_FL):
        sorties = rng.integers(min_sorties_FL, max_sorties_FL)
        pilot = self.add_EXP_pilot(f16_sorties=sorties, tos=0, quals=ug_quals[:2])
        new_nth_pilots.append(pilot)

      num_API6_IP = rng.binomial(num_API6, prop_API6_IP)
      for _ in range(num_API6):
        sorties = rng.integers(min_sorties_FL, max_sorties_IP)
        my_quals = ug_quals[:2]

        if num_API6_IP > 0:
          my_quals += [ug_quals[-1]]
          num_API6_IP -= 1
        pilot = self.add_EXP_pilot(f16_sorties=sorties, tos=0, api_category=6, quals=my_quals)
        new_nth_pilots.append(pilot)

      for _ in range(num_IP):
        sorties = rng.integers(min_sorties_IP, max_sorties_IP)
        pilot = self.add_EXP_pilot(f16_sorties=sorties, tos=0, quals=ug_quals)
        new_nth_pilots.append(pilot)

      return new_nth_pilots

    def inflow_first_tour(self, num_API1):
      new_pilots = []

      for _ in range(num_API1):
        ftu_sortie_delta = rng.integers(-5, 11)
        pilot = self.add_INX_pilot(f16_sorties=ftu_sortie_delta, quals=[])
        new_pilots.append(pilot)

      return new_pilots

    def outflow_pilots(self):
      tos_cap = 32
      pids_tos_exceeded = [id for id in self.pilots 
                           if self.pilots[id].return_tos() >= tos_cap]
      self.remove_pilots(pids_tos_exceeded)

    def get_pilots_qualified_as(self, qual):
      return {id: pilot for id, pilot in self.pilots.items() if pilot.return_highest_qual() == qual}

    def get_students_in(self, ug):
      return {id: pilot for id, pilot in self.pilots.items() if pilot.return_upgrade() == ug}

    def summarize(self):
      roster_API1 = {k: p for k, p in self.pilots.items() if p.return_api() == 1}

      num_EXP = np.sum([p.return_experience() for p in roster_API1.values()])
      num_INX = len(roster_API1) - num_EXP
      exp_pct = num_EXP / (num_EXP + num_INX)
      
      upgrades = [p.return_upgrade() for p in roster_API1.values()]
      highest_quals = [p.return_highest_qual() for p in roster_API1.values()]
      num_MQT = upgrades.count(ug_names[0])
      num_FLUG = upgrades.count(ug_names[1])
      num_IPUG = upgrades.count(ug_names[2])
      num_WG = highest_quals.count(ug_quals[0])
      num_FL = highest_quals.count(ug_quals[1])
      num_IP = highest_quals.count(ug_quals[2])

      print(f'{self.sq_name} SUMMARY:')
      print(
          f'API-1 ({len(roster_API1)}) >> '
          f'EXP: {num_EXP} / INX: {num_INX} | EXP% (API-1): {exp_pct:.2f} | '
          f'API-6: {len(self.pilots)-len(roster_API1)} | '
          f'{ug_quals[0]}: {num_WG} (+{num_MQT} in {ug_names[0]}) / '
          f'{ug_quals[1]}: {num_FL} (+{num_FLUG} in {ug_names[1]}) / '
          f'{ug_quals[2]}: {num_IP} (+{num_IPUG} in {ug_names[2]}) ')

    
    def print_sq(self):
        print(f'{self.sq_name} ROSTER:')
        for p in self.pilots.values():
          print(p.summarize())