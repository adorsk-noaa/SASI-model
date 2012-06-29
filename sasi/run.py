import sasi.conf as conf
from sasi.dao import CSV_DAO, SHP_DAO, SA_DAO
from sasi.domain import Cell, Feature, Substrate, Habitat, Gear, VulnerabilityAssessment
from sasi.domain.effort_models import NominalEffortPerGearModel
from sasi.domain import SASI_Model

import sasi.sa as sa
import sasi.sa.domain

import sasi.util.georefine
import shapely.wkt, shapely.wkb

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

    # Ingest/generate raw data.
    #cells_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'cells.shp')
    #cells_dao = SHP_DAO(shp_file=cells_shp_file, model=Cell, limit=None)
    cells_dao = SA_DAO(session=sa.session, primary_class=Cell)

    #habs_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'habitats.shp')
    #habs_dao = SHP_DAO(shp_file=habs_shp_file, model=Habitat, limit=None)
    habs_dao = SA_DAO(session=sa.session, primary_class=Habitat)

    substrates_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'substrates.csv')
    substrates_dao = CSV_DAO(csv_file=substrates_csv_file, model=Substrate)

    features_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'features.csv')
    features_dao = CSV_DAO(csv_file=features_csv_file, model=Feature)

    gears_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'gears.csv')
    gears_dao = CSV_DAO(csv_file=gears_csv_file, model=Gear)

    va_csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'va.csv')
    va_reader = csv.DictReader(open(va_csv_file,'rb'))
    va_rows = []
    for r in va_reader:
        # Map dry gear codes to categories.
        r['GEAR_CATEGORY'] = conf.conf['dry_code_to_gear_category'].get(r['GEAR_CODE'])
        va_rows.append(r)
    va = VulnerabilityAssessment(rows=va_rows)	

    # Prepare data (merging, filtering, calculating derived properties).
    #calculate_cell_compositions(cells_dao, habs_dao)

    # Setup effort model.
    use_gears = gears_dao.all()[0:1]
    effort_model = NominalEffortPerGearModel(cell_source=cells_dao, gears=use_gears, times=times)

    sasi_model = SASI_Model(t0=t0, tf=tf, dt=dt, cell_source=cells_dao, feature_source=features_dao, effort_model=effort_model, va=va)
    sasi_model.run()

    """
    for t, t_results in sasi_model.results_t_c.items():
        print "t: %s" % (t)
        for cell, tc_results in t_results.items():
            print " cell: %s" % (cell.id)
            for r in tc_results.values():
                fields = ['a','x','y','z','znet']
                print "  %s" % ",".join(["%s: %.2f" % (f, getattr(r,f)) for f in fields])
    """

    if conf.conf['verbose']: print >> sys.stderr, "Creating georefine package..."

    # Create GeoRefine package.
    georefine_package = create_georefine_package(
            cells=cells_dao.all(), 
            substrates=substrates_dao.all(), 
            features=features_dao.all(), 
            gears=gears_dao.all(), 
            results=sasi_model.results
            )

    print "Generated georefine package is: %s" % georefine_package
    print "Done."


# Calculate cell habitat compositions, taking advantage of
# PostGIS functions.
def calculate_cell_compositions(cells_dao, habs_dao):

    # Save cells, habitats to temporary tables in the db.
    # This can take a bit of time.
    if conf.conf['verbose']: print >> sys.stderr, "Creating temp cell/hab tables..."
    tables = ['cell', 'habitat']
    for table in tables:
        sa.metadata.tables[table].drop(bind=sa.engine, checkfirst=True)
        sa.metadata.tables[table].create(bind=sa.engine)
    sa.session.add_all([c for c in cells_dao.all()])
    sa.session.add_all([h for h in habs_dao.all()])
    sa.session.commit()

    # Calculate areas for habitats.
    if conf.conf['verbose']: print >> sys.stderr, "Calculating habitat areas..."
    for hab in habs_dao.all():
        hab_area_entity = geo_func.area(func.geography(Habitat.geom))
        hab.area = sa.session.query(hab_area_entity).filter(Habitat.id == hab.id).one()[0]
        sa.session.add(hab)
    sa.session.commit()

    # Generate habitat compositions for cells.
    counter = 0
    for cell in cells_dao.all():
        if conf.conf['verbose']:
            if (counter % 100) == 0: print >> sys.stderr, "at cell # %s" % counter

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
        sa.session.add(cell)

        counter += 1

    sa.session.commit()

    """
    # Remove the temporary tables.
    for t in tables:
        sa.metadata.tables[table].drop(bind=sa.engine, checkfirst=True)
    """

def create_georefine_package(cells=[], substrates=[], features=[], gears=[], results=[]):

    # Define a geometry formatter.
    def geom_formatter(cell):
        return shapely.wkt.dumps(shapely.wkb.loads("%s" % cell.geom.geom_wkb))

    # Create data files.
    data_files = []

    # Cells.
    cells_data_file = sasi.util.georefine.objects_to_csv_file(
            objects=cells,
            fields=[ 'id', 'area', {'name': 'geom', 'formatter': geom_formatter}]
            )
    data_files.append({'name': 'cell.csv', 'path': cells_data_file})

    # Substrates.
    substrates_data_file = sasi.util.georefine.objects_to_csv_file(
            objects=substrates,
            fields=[ 'id', 'name'] 
            )
    data_files.append({'name': 'substrate.csv', 'path': substrates_data_file})

    # Features.
    features_data_file = sasi.util.georefine.objects_to_csv_file(
            objects=features,
            fields=[ 'id', 'name', 'category'] 
            )
    data_files.append({'name': 'feature.csv', 'path': features_data_file})

    # Gears.
    gears_data_file = sasi.util.georefine.objects_to_csv_file(
            objects=gears,
            fields=[ 'id', 'name', 'category'] 
            )
    data_files.append({'name': 'gear.csv', 'path': gears_data_file})

    # Results.
    results_data_file = sasi.util.georefine.objects_to_csv_file(
            objects=results,
            fields=[ 'id', 't', 'cell_id', 'gear_id', 'substrate_id', 'feature_id',
                'a', 'x', 'y', 'z', 'znet'] 
            )
    data_files.append({'name': 'result.csv', 'path': results_data_file})

    # Create georefine tar.gz, including app config and schema.
    georefine_tgz = sasi.util.georefine.create_gr_project_file(
            schema_file=conf.conf['results_georefine_schema'],
            app_config_file=conf.conf['results_georefine_app_config'],
            data_files=data_files
            )

    return georefine_tgz


if __name__ == '__main__':
    main()
