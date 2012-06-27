import sasi.conf as conf
from sasi.dao.shp_dao import SHP_DAO
from sasi.domain.cell import Cell
from sasi.domain.habitat import Habitat

from datetime import datetime
import sys
import os
import csv

import fiona
import shapely.geometry 


def main():
    conf.conf['verbose'] = True




    cells_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'cells.shp')
    c = fiona.collection(cells_shp_file, 'r')
    c2 = fi
    
    return
    cells_dao = SHP_DAO(shp_file=cells_shp_file, model=Cell)

    habs_shp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_data', 'habitats.shp')
    habs_dao = SHP_DAO(shp_file=habs_shp_file, model=Habitat)

    # Build binary-tree lookup to speed up intersection searches.
    cell_collection = fiona.collection(cells_shp_file, 'r')
    btree = create_spatial_btree(cell_collection.bounds, cur_level=1, num_levels=4)
    # Index habitats with the tree.
    for hab in habs_dao.all():
        leafs = get_leafs_for_geom(btree, hab.geom)
        for leaf in leafs:
            leaf_habs = leaf.setdefault('habitats', [])
            leaf_habs.append(hab)

    # Generate habitat compositions for cells.
    for cell in cells_dao.all():
        composition = {}
        # Get habitats in the neighborhood of the cell.
        leafs = get_leafs_for_geom(btree, cell.geom)
        local_habs = []
        for leaf in leafs:
            local_habs.extend(leaf.get('habitats', []))

        # Scan local habitats...
        for hab in local_habs:
            # Calculate pct area if habitat intersects the cell.
            if hab.geom.intersects(cell.geom):
                hab_key = (hab.substrate, hab.energy,)
                pct_area = hab.geom.intersection(cell.geom).area/cell.geom.area
                composition[hab_key] = composition.get(hab_key, 0) + pct_area
        cell.habitat_composition = composition

        if not cell.habitat_composition:
            print cell.type_id

                
def create_spatial_btree(bounds, cur_level=1, num_levels=2):
    node = {}

    # Get ranges.
    x_min = bounds[0]
    x_max = bounds[2]
    x_range = x_max - x_min
    y_min = bounds[1]
    y_max = bounds[3]
    y_range = y_max - y_min

    # Create geom from bounds.
    node['geom'] = shapely.geometry.shape({
        'type': 'Polygon',
        'coordinates': [[
            (x_min, y_min),
            (x_min, y_max),
            (x_max, y_max),
            (x_max, y_min),
            (x_min, y_min)
        ]]
    }) 

    # Create subtrees for sub-bounds if not at last level.
    if not cur_level == num_levels:
        children = []
        for i in range(2):
            for j in range(2):
                sub_x_min = x_min + i * x_range/2.0
                sub_x_max = x_min + (i+1) * x_range/2.0
                sub_y_min = y_min + j * x_range/2.0
                sub_y_max = y_min + (j+1) * x_range/2.0
                sub_bound = (sub_x_min, sub_y_min, sub_x_max, sub_y_max,)
                children.append(create_spatial_btree(sub_bound, cur_level + 1, num_levels))
        node['children'] = children

    return node

def get_leafs_for_geom(node, geom):
    leafs = []
    if node.has_key('children'):
        for child in node['children']:
            if geom.intersects(child['geom']):
                leafs.extend(get_leafs_for_geom(child, geom))
    else:
        leafs.append(node)
    return leafs







            
        





if __name__ == '__main__':
    main()
