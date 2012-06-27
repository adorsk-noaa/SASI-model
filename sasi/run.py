import sasi.conf as conf
from sasi.dao.csv_dao import CSV_DAO
from sasi.domain.cell import Cell
from sasi.domain.feature import Feature
from sasi.domain.gear import Gear
from sasi.domain.va import VulnerabilityAssessment
from sasi.domain.effort_models.nominal_effort_per_gear_model import NominalEffortPerGearModel
from sasi.domain.sasi_model import SASI_Model

from datetime import datetime
import sys
import os
import csv


def main():
    conf.conf['verbose'] = True

    t0 = 2008
    tf = 2010
    dt = 1
    times = range(t0,tf+1,dt)

    cells_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'cells.csv')
    cells_dao = CSV_DAO(csv_file=cells_csv_file, model=Cell)

    features_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'features.csv')
    features_dao = CSV_DAO(csv_file=features_csv_file, model=Feature)

    gears_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'gears.csv')
    gears_dao = CSV_DAO(csv_file=features_csv_file, model=Gear)

    use_gears = gears_dao.all()[0:1]
    effort_model = NominalEffortPerGearModel(cell_source=cells_dao, gears=use_gears, times=times)

    va_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'va.csv')
    va_reader = csv.DictReader(open(va_csv_file,'rb'))
    va_rows = []
    for r in va_reader:
        # Map dry gear codes to categories.
        r['GEAR_CATEGORY'] = conf.conf['dry_code_to_gear_category'].get(r['GEAR_CODE'])
        va_rows.append(r)
    va = VulnerabilityAssessment(rows=va_rows)	

    sasi_model = SASI_Model(t0=t0, tf=tf, dt=dt, cell_source=cells_dao, feature_source=features_dao, effort_model=effort_model, va=va)
    



if __name__ == '__main__':
    main()
