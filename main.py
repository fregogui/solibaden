from maps import load_map
from resolver import graph_resolver, naive_resolver

CSV_MAP_PATH = "/Users/gfregosi/PycharmProjects/solibaden/maps/lamor.csv"

original_map = load_map(CSV_MAP_PATH)

# naive_resolver(original_map=original_map)
graph_resolver(original_map=original_map, max_iteration=1000000)



