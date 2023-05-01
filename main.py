from maps import load_map
from resolver import naive_resolver

CSV_MAP_PATH = "/Users/gfregosi/PycharmProjects/solibaden/maps/demo.csv"

original_map = load_map(CSV_MAP_PATH)

naive_resolver(original_map=original_map)
