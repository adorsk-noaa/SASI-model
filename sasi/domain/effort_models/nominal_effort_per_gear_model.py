from sasi.domain.effort import Effort

class NominalEffortPerGearModel(object):

    def __init__(self, cell_source=None, gears=[], times=[]):
        self.cell_source = cell_source
        self.gears = gears
        self.times = times

    def get_efforts(self, filters=None):
        efforts = []
        for c in self.cell_source.all():
            for t in self.times:
                efforts.extend(self.get_efforts_for_c_t(cell=c, time=t))
        return efforts

    def get_efforts_for_c_t(self, cell=None, time=None):

        # Initialize a list of efforts.
        efforts = []

        # Set the nominal effort to be the cell's area.
        nominal_effort = cell.area

        # Get the list of gears.
        gears = self.gears

        # For each gear...
        for gear in gears:

            # Create an effort for the gear.
            efforts.append(Effort(cell=cell, time=time, gear=gear, swept_area=nominal_effort, hours_fished=None))

        return efforts

