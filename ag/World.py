from ag.ECS import Entity, System


class World(Entity):

    def __init__(self, name=None, uid=None):
        super().__init__(self)
        self.name = name if name else 'world'
        self.systems = []
        self.map = None
        self.active_area = (0, 0)

    def update(self):

        self.update_active_area()
        self.update_inactive_areas()

    def update_area(self, coord):

        for system in self._map.grid[coord].systems:
            system.update()

    def update_active_area(self):
        return self.update_area(self.active_area)

    def update_inactive_areas(self):
        for coord in self._map.grid.items():
                if coord != self.active_area:
                    self.update_area(coord)

    def add_system(self, system):

        if isinstance(system, System):
            self.systems.append(system)
        else:
            raise TypeError("The variable {} is not a system, it's a {}"
                            .format(system, type(system)))
