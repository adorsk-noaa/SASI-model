import sasi.conf as conf
from sasi.dao import CSV_DAO, SHP_DAO
from sasi.domain import Cell, Feature, Habitat, Gear, VulnerabilityAssessment
from sasi.domain.effort_models import NominalEffortPerGearModel
from sasi.domain import SASI_Model

import sasi.sa as sa
import sasi.sa.domain

from geoalchemy.functions import functions as geo_func
from sqlalchemy import func

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

    """
    # Read in data from inputs.
    cells_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'cells.shp')
    cells_dao = SHP_DAO(shp_file=cells_shp_file, model=Cell, limit=None)

    habs_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'habitats.shp')
    habs_dao = SHP_DAO(shp_file=habs_shp_file, model=Habitat, limit=None)
    """

    calculate_cell_compositions(None, None)


    """
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
    """
    

# Calculate cell habitat compositions, taking advantage of
# PostGIS functions.
def calculate_cell_compositions(cells_dao, habs_dao):

    """
    # Save cells, habitats to temporary tables in the db.
    # This can take a bit of time.
    tables = ['cell', 'habitat']
    for table in tables:
        sa.metadata.tables[table].drop(bind=sa.engine, checkfirst=True)
        sa.metadata.tables[table].create(bind=sa.engine)
    sa.session.add_all([c for c in cells_dao.all()])
    sa.session.add_all([h for h in habs_dao.all()])
    sa.session.commit()
    """

    # Generate habitat compositions for cells.
    counter = 0
    #for cell in cells_dao.all():
    for cell in sa.session.query(Cell).all():
        if conf.conf['verbose']:
            if (counter % 100) == 0: print >> sys.stderr, "at cell # %s", counter
        counter += 1

        composition = {}

        # Get cell area.
        cell_area_entity = geo_func.area(func.geography(Cell.geom))
        cell.area = sa.session.query(cell_area_entity).filter(Cell.id == cell.id).one()[0]

        # Get habitats which intersect the cell.
        intersection_area_entity = geo_func.area(func.geography(geo_func.intersection(Habitat.geom, cell.geom)))
        results = sa.session.query(Habitat, intersection_area_entity).filter(Habitat.geom.intersects(cell.geom)).all()
        for result in results:
            hab = result[0]
            intersection_area = result[1]
            hab_key = (hab.substrate, hab.energy,)
            pct_area = intersection_area/cell.area
            composition[hab_key] = composition.get(hab_key, 0) + pct_area

        cell.habitat_composition = composition

    """
    # Remove the temporary tables.
    for t in tables:
        sa.metadata.tables[table].drop(bind=sa.engine, checkfirst=True)
    """


if __name__ == '__main__':
    main()
