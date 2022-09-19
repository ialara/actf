# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 16:09:05 2022

@author: ilara
"""
import pytest
from context import absorption
from absorption import pilot

@pytest.fixture
def my_pilot():
    return pilot.Pilot(0, f16_sorties=200, quals=[], tos=0)

def test_fly_sortie_increments_sortie_count_by_one(my_pilot):
    my_pilot.fly_sortie()
    assert my_pilot.f16_sorties == 201
    
def test_increment_tos_defaults_increment_of_one(my_pilot):
    my_pilot.increment_tos()
    assert my_pilot.tos == 1

def test_increment_tos_positive_integer(my_pilot):
    my_pilot.increment_tos(5)
    assert my_pilot.tos == 5
    
def test_increment_tos_positive_float(my_pilot):
    my_pilot.increment_tos(3.5)
    assert my_pilot.tos == pytest.approx(3.5)
    
def test_increment_tos_negative_integer_decrements(my_pilot):
    my_pilot.tos = 4
    my_pilot.increment_tos(-2)
    assert my_pilot.tos == 2
    
def test_increment_tos_negative_float_decrements(my_pilot):
    my_pilot.tos = 5
    my_pilot.increment_tos(-2.5)
    assert my_pilot.tos == pytest.approx(2.5)

def test_increment_tos_prevents_negative_tos_integer(my_pilot):
    my_pilot.increment_tos(-1)
    assert my_pilot.tos == 0
    
def test_increment_tos_prevents_negative_tos_float(my_pilot):
    my_pilot.increment_tos(-0.1)
    assert my_pilot.tos == 0
    
def test_increment_tos_below_zero_gives_warning(my_pilot, mocker):
    mocked_func = mocker.patch('absorption.pilot.Pilot.log_warn')
    my_pilot.increment_tos(-0.1)
    mocked_func.assert_called_once()
    
def test_increment_tos_non_numeric_raises_TypeError(my_pilot):
    with pytest.raises(TypeError):
        my_pilot.increment_tos('foo')
    
def test_award_valid_qualification(my_pilot):
    qual = 'FL'
    my_pilot.award_qual(qual)
    assert qual in my_pilot.quals
    
def test_award_duplicate_qualification_does_not_duplicate(my_pilot):
    qual = 'FL'
    my_pilot.award_qual(qual)
    my_pilot.award_qual(qual)
    assert my_pilot.quals.count(qual) == 1
    
def test_award_duplicate_qualification_gives_warning(my_pilot, mocker):
    qual = 'FL'
    mocked_func = mocker.patch('absorption.pilot.Pilot.log_warn')
    my_pilot.award_qual(qual)
    my_pilot.award_qual(qual)
    mocked_func.assert_called_once()
    
@pytest.mark.xfail # Not Implemented
def test_award_invalid_qualification_is_rejected(my_pilot):
    qual = 'bad qualification'
    my_pilot.award_qual(qual)
    assert qual not in my_pilot.quals

@pytest.mark.xfail # Not Implemented
def test_award_invalid_qualification_gives_warning(my_pilot, mocker):
    qual = 'bad qualification'
    mocked_func = mocker.patch('absorption.pilot.Pilot.log_warn')
    my_pilot.award_qual(qual)
    mocked_func.assert_called_once()
    
# if __name__ == '__main__':
#     pytest.main(["-v"])