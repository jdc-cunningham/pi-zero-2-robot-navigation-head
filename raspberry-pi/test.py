from map.map import Map

world = Map()

# world.plot_map()

scan_plane = world.ScanPlane(0.0, 1.0, 1.0, 2.0, 3.0, 0.0)

world.rotate_plane(0, world.get_plane_vertices(scan_plane))
