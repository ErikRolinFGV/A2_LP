class tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size = tile_size
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': "grass", 'variant': 1, "pos": (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': "stone", 'variant': 1, "pos": (10, 5 + i)}
    
    def render(self, surfice):
        for tile in self.offgrid_tiles:
            surfice.blit(self.game.assets[tile["type"]][tile["variant"]], tile['pos'])
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surfice.blit(self.game.assets[tile["type"]][tile["variant"]], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))



