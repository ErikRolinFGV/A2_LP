import pygame

# Deslocamento dos vizinhos
Neighbor_OFFSET = [(-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
physics_tiles = ['grass', 'stone']  # Tipos de tiles com física

class tilemap:
    def __init__(self, game, tile_size=16):
        self.tile_size = tile_size  # Tamanho dos tiles
        self.game = game  # Referência ao jogo principal
        self.tilemap = {}  # Dicionário para armazenar tiles
        self.offgrid_tiles = []  # Tiles fora do grid

        # Preenchendo o tilemap com tiles de exemplo
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': "grass", 'variant': 1, "pos": (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': "stone", 'variant': 1, "pos": (10, 5 + i)}
    
    # Obtém os tiles próximos de uma posição
    def tiles_collision(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in Neighbor_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles  # Retorna a lista de tiles encontrados
        
    # Obtém os retângulos para tiles com física
    def physics_rects_collision(self, pos):
        rects = []
        for tile in self.tiles_collision(pos):
            if tile['type'] in physics_tiles:  # Verifica se o tile está na lista de física
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size, 
                    tile['pos'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                ))
        return rects  # Retorna os retângulos para colisão
    
    # Renderiza os tiles na superfície
    def render(self, surface, offset=(0,0)):
        # Renderiza tiles fora do grid
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        # Renderiza tiles no grid
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1])
            )




