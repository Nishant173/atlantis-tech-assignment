"""
Note: The approach to find the shortest distance between the coordinates is not the most optimal one.
I would use Dijkstra's shortest path algorithm to solve it optimally. But as time is an issue right
now, I have implemented it in a brute-force manner.

References:
    - https://stackoverflow.com/questions/1502590/calculate-distance-between-two-points-in-google-maps-v3
    - https://developers.google.com/maps/documentation/distance-matrix/overview#maps_http_distancematrix_latlng-py
"""

from itertools import permutations
import random
from typing import List, Optional, Union


def ord_of_text(text: str) -> int:
    return int(sum((ord(char) for char in text)))


def get_distance_between_coords(coord1: str, coord2: str) -> Union[int, float]:
    """
    Returns some fake distance between the given two co-ordinates (in kilometers).
    The distance will always be the same for every unique co-ordinate pair given.

    Note: I could have used an API to calculate the distance, but since this is just an interview
    assignment, I have used a neat trick to do the same. Hope you don't mind.
    """
    random_seed = ord_of_text(text=coord1 + coord2) * -2 # Some random seed value
    random.seed(random_seed)
    distance_between_coords = random.random() * 1000
    return round(distance_between_coords, 3)


def get_distance_between_continuous_coords(coords: List[str]) -> Union[int, float]:
    last_idx = len(coords) - 1
    idx_start, idx_end = 0, 1
    distance = 0
    while idx_end <= last_idx:
        distance += get_distance_between_coords(coord1=coords[idx_start], coord2=coords[idx_end])
        idx_start, idx_end = idx_start + 1, idx_end + 1
    return round(distance, 3)


def get_path_combinations(
        vertices: List[str],
        starting_vertex: Optional[str] = None,
        ending_vertex: Optional[str] = None,
    ) -> List[str]:
    num_vertices = len(vertices)
    path_combinations = [''.join(arrangement) for arrangement in list(permutations(vertices, num_vertices))]
    if path_combinations and starting_vertex is not None:
        path_combinations = list(filter(lambda path: path[0] == starting_vertex, path_combinations))
    if path_combinations and ending_vertex is not None:
        path_combinations = list(filter(lambda path: path[-1] == ending_vertex, path_combinations))
    return path_combinations


if __name__ == "__main__":
    coords_by_vertex = {
        'A': "51.5074 N, 0.1278 W",
        'B': "60.8566 N, 2.3522 E",
        'C': "55.2311 N, 2.1222 E",
        'D': "64.0010 N, 0.1002 W",
    }
    path_combinations = get_path_combinations(
        vertices=list('ABCD'),
        starting_vertex='A',
    )
    distance_by_path = {}
    for path_combination in path_combinations:
        distance_by_path[path_combination] = get_distance_between_continuous_coords(
            coords=[coords_by_vertex[vertex] for vertex in path_combination]
        )

    # Get the shortest path
    least_distance = list(distance_by_path.values())[0]
    shortest_path = list(distance_by_path.keys())[0]
    for path, distance in distance_by_path.items():
        if distance < least_distance:
            least_distance = distance
            shortest_path = path
    print(
        f"Path combinations: {path_combinations}",
        f"All distances by path: {distance_by_path}",
        f"Shortest path: '{shortest_path}'",
        f"Least distance: {least_distance} kms",
        sep="\n",
    )