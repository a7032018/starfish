from typing import Mapping, Optional, List, Tuple

from starfish.core.types import Axes, Coordinates, SpotAttributes


AXES_ORDER = (Axes.ROUND, Axes.CH)


class SpotFindingResults:
    """
    Wrapper class that describes the results from a spot finding method. The
    results dict is a collection of (round,ch indices) and their corresponding measured
    SpotAttributes.
    """

    def __init__(self, imagestack, spot_attributes_list: Optional[List[Tuple]] = None):
        """
        Construct a SpotFindingResults instance

        Parameters
        -----------
        spot_attributes_list : Optional[List[Tuple[indices, SpotAttributes]]]
            If spots were fond using Imagestack.transform() the result is a list of
            tuples (indices, SpotAttributes). Instantiating SpotFindingResults with
            this list will convert the information to a dictionary.
        """
        if spot_attributes_list:
            for indices, spots in spot_attributes_list:
                self._results[indices] = spots
        else:
            self._results: Mapping[Tuple, SpotAttributes] = dict()
        self.physical_coord_ranges = {
            Axes.X: imagestack.xarray[Coordinates.X.value],
            Axes.Y: imagestack.xarray[Coordinates.Y.value],
            Axes.Z: imagestack.xarray[Coordinates.Z.value]}

    def set_tile_spots(self, indices: Mapping[Axes, int], spots: SpotAttributes
                       ) -> None:
        """
        Add the tile indices and corresponding SpotAttributes to the results dict.

        Parameters
        ----------
        indices: Mapping[Axes, int]
            Mapping of Axes to int values
        spots: SpotAttributes
            Describes spots found on this tile.
        """
        tile_index = tuple(indices[i] for i in AXES_ORDER)
        self._results[tile_index] = spots

    def get_tile_spots(self, indices: Mapping[Axes, int]) -> SpotAttributes:
        """
        Returns the spots found on a given tile.

        Parameters
        ----------
        indices: Mapping[Axes, int]
            Mapping of Axes to int values

        Returns
        --------
        SpotAttributes
        """
        round_ch_index = tuple(indices[i] for i in AXES_ORDER)
        return self._results[round_ch_index]

    def round_ch_indices(self):
        """
        Return all tile indices.
        """
        return self._results.keys()

    def all_spots(self):
        """
        Return all SpotAttributes
        """
        return self._results.values()

    def round_labels(self):
        """
        Return the set of Round labels in the SpotFindingResults
        """
        return list(set(sorted(r for (r, ch) in self.round_ch_indices())))

    def ch_labels(self):
        """
        Return the set of Ch labels in the SpotFindingResults
        """
        return list(set(sorted(ch for (c, ch) in self.round_ch_indices())))

    def get_physical_coord_range(self, axes: Axes):
        return self.physical_coord_ranges[axes]