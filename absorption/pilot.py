# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:15:02 2022

@author: ilara
"""

class Pilot:
    """An Air Force F-16 pilot that fills squadron billets"""
    # Syllabus lengths (number of UP sorties)
    syllabi_rides = {ug: dur for ug, dur in zip(ug_names, ug_rides)}

    # Quals awarded when completing upgrades
    ug_awards = {ug: q for ug, q in zip(ug_names, ug_quals)}

    # Everyone gets these many sorties from FTU
    ftu_sorties = 59 # Avg based on 49 WG PA release: https://bit.ly/3R8aADh

    # Definition of experience
    exp_sorties = 250
    exp_qual = ug_quals[1] # FL

    def __init__(self, id, f16_sorties, tos, api_category, quals=[], ug=None):
        self.id = id
        self.f16_sorties = self.ftu_sorties + f16_sorties
        self.tos = tos
        self.quals = quals
        self.is_exp = False
        self.check_experience()
        self.api_category = 1 if not self.is_exp else api_category
        self.ug = None
        if ug is not None:
            self.enroll_upgrade(ug)

    def log(self, msg, prefix='>>'):
        print(f'{prefix} PID {self.id} {msg}')

    def enroll_upgrade(self, ug):
        assert self.ug is None, 'Pilot already enrolled in upgrade'
        assert ug in self.ug_awards, 'Invalid upgrade specified'
        assert self.ug_awards[ug] not in self.quals, 'Pilot already completed upgrade'
        self.ug = ug
        self.ride_num = 0
        self.pending_qual = self.ug_awards[self.ug]
        self.log(f'enrolled in {self.ug}')

    def disenroll_upgrade(self):
        prev_ug = self.ug
        self.ug = None
        self.log(f'disenrolled from: {prev_ug}', prefix='<<')

    def fly_ug_sortie(self):
        assert self.ug is not None, 'Pilot not enrolled in upgrade'
        self.ride_num += 1
        if self.check_ug_complete(self.ug, self.ride_num):
          self.award_qual(self.pending_qual)
          self.disenroll_upgrade()
        self.fly_sortie()

    def check_ug_complete(self, ug, ride):
        return ride == self.syllabi_rides[ug]

    def fly_sortie(self):
        self.f16_sorties += 1
        self.check_experience()

    def award_qual(self, qual):
        assert qual in self.ug_awards.values(), 'Invalid qualification specified'
        assert qual not in self.quals, 'Pilot already qualified'
        self.quals.append(qual)
        self.log(f'awarded: {qual}', prefix='++')
        self.check_experience()

    def remove_qual(self, qual):
        assert qual in self.quals, 'Pilot does not have this qualification'
        self.quals.remove(qual)
        self.log(f'un-awarded: {qual}', prefix='--')
        self.check_experience()

    def check_experience(self):
        prev_status = self.is_exp
        self.is_exp = (self.f16_sorties >= self.exp_sorties and 
                      self.exp_qual in self.quals)
        if self.is_exp and not prev_status:
            self.log('EXPERIENCED', prefix='**')

    def increment_tos(self, months=1):
      assert isinstance(months, (int, float)), 'Months must be numeric'
      self.tos += months

    def return_experience(self):
      return self.is_exp

    def return_upgrade(self):
      return self.ug

    def return_api(self):
      return self.api_category

    def return_highest_qual(self):
      if self.quals == []:
        return ''
  
      return self.quals[-1]

    def return_tos(self):
      return self.tos

    def summarize(self):
        text = 'PID {:2d}: {}{} | SOR: {:4d} | TOS: {:04.1f} mo. | QL: {}'.format(self.id,
                                                            '6-' if self.api_category == 6 else '',
                                                            'EXP' if self.is_exp else 'INX',
                                                            self.f16_sorties,
                                                            self.tos,
                                                            self.quals)
        if self.ug is not None:
            text += f' | UG: {self.ug} #{self.ride_num + 1}' # +1 to show next (pending) ride
            if self.ride_num == self.syllabi_rides[self.ug] - 1:
              text += ' (CERT)'
        return text