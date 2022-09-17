# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:15:02 2022

@author: ilara
"""
from .syllabus import ExperiencedBadge

class Pilot:
    """An Air Force F-16 pilot that fills squadron billets"""
    # Default 59 sorties is avg from FTU based on 49 WG PA release: https://bit.ly/3R8aADh
    def __init__(self, id, f16_sorties=59, tos=0, api_category=1, quals=[], ug=None):
        self.id = id
        self.f16_sorties = f16_sorties
        self.tos = tos
        self.quals = quals
        self.is_exp = False
        #self.check_experience()
        self.api_category = 1 if not self.is_exp else api_category
        self.ug = None
        if ug is not None:
            self.enroll_upgrade(ug)

    def log(self, msg, prefix='>>'):
        print(f'{prefix} PID {self.id} {msg}')
        
    def log_warn(self, msg, prefix='WARNING: '):
        self.log(msg)

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

    def award_qual(self, qual):
        #assert qual in self.ug_awards.values(), 'Invalid qualification specified'
        if qual in self.quals:
            warn_msg = f'Duplicate qual attempt - Pilot {self.id} already \
                         qualified as {qual}. Did nothing.'
            self.log_warn(warn_msg)
            return
        
        self.quals.append(qual)
        self.log(f'awarded: {qual}', prefix='++')

    def remove_qual(self, qual):
        assert qual in self.quals, 'Pilot does not have this qualification'
        self.quals.remove(qual)
        self.log(f'un-awarded: {qual}', prefix='--')

    def check_experience(self):
        prev_status = self.is_exp
        self.is_exp = ExperiencedBadge.is_experienced(self)
        if self.is_exp and not prev_status:
            self.log('EXPERIENCED', prefix='**')

    def increment_tos(self, months=1):
      if not isinstance(months, (int, float)):
          raise TypeError('Months must be numeric')
      self.tos += months
      if self.tos < 0:
          self.tos = 0
          warn_msg = f'Pilot {self.id} attempt to set negative TOS. Set TOS to {self.tos}.'
          self.log_warn(warn_msg)
      
    def get_sorties(self):
        return self.f16_sorties
    
    def get_quals(self):
        return self.get_quals()

    def return_experience(self):
      return self.is_exp

    def get_upgrade(self):
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