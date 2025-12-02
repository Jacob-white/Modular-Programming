import sys
import os

print("Sys Path:", sys.path)
print("CWD:", os.getcwd())

try:
    import src
    print("Src file:", src.__file__)
except ImportError as e:
    print("ImportError src:", e)

try:
    from src.analytics import geospatial
    print("Geospatial file:", geospatial.__file__)
    print("Dir geospatial:", dir(geospatial))
except ImportError as e:
    print("ImportError geospatial:", e)

try:
    from src.analytics.geospatial import haversine_distance
    print("Successfully imported haversine_distance")
except ImportError as e:
    print("ImportError haversine_distance:", e)
