from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from shapely.geometry import Point


class Routing(ABCMeta):
    @abstractmethod
    def get_route(
            self,
            waypoints: List[Tuple[float, float], Point],
            **kwargs):
        pass

