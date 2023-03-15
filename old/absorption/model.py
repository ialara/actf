# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:16:38 2022

@author: ilara
"""

import numpy as np
#from pilot import Pilot
#from squadron import SquadronRoster
#from crew import FlightCrew
#from fly_order import FlySchedule
from syllabus import Syllabus

rng = np.random.default_rng()

syllabi_names = ['MQT', 'FLUG', 'IPUG']
syllabi_durations = [9,  9,      9]
syllabi_awards = ['WG',  'FL',  'IP']

syllabi = []

for syllabus in zip(syllabi_names, syllabi_durations, syllabi_awards):
    syllabi.append(Syllabus(*syllabus))
    
[s.print_() for s in syllabi]

# Simulation parameters

# --Start run
# Squadron initialization
# Warmup (x months)
# ----Start month
# Determine training capacity
# Prioritize pilots/missions
# Schedule missions
# Fly missions
# Update qualifications
# Inflows/outflows
# Start trial (32 months)
# Collect output statistics
# --Finish runs
# Summarize simulation