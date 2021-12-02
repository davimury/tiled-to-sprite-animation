import os
import json
from itertools import product
from PIL import Image

class ExportSprite:
    def __init__(self, tiled_map_path: str = './tiled_files/tilemap.json', map_data_path: str = './tiled_files/mapdata.json') -> None:
        self.tilemap = self._load_tiled_map_file(tiled_map_path)
        self.mapdata = self._load_map_data_file(map_data_path)
        self.tileset = Image.open('./tiled_files/tileset.png')
        self.generate_animated_sprite_sheet()

    def _load_tiled_map_file(self, tiled_map_path):
        with open(tiled_map_path, encoding = 'utf-8') as f:
            return json.load(f)
 
    def _load_map_data_file(self, map_data_path):
        with open(map_data_path, encoding = 'utf-8') as f:
            return json.load(f)
    
    def _get_map_matrix(self):
        matrixes = []
        for value in self.mapdata['layers']:
            tmp = {}
            for data_key, data_value in enumerate(value['data']):
                tmp[data_key] = data_value
            matrixes.append(tmp)
        return matrixes

    def _get_tile_by_id(self, value):
        w, h = self.tileset.size
        d = self.tilemap['tilewidth']
        for idx, (i, j) in enumerate(product(range(0, h-h%d, d), range(0, w-w%d, d))):
            if idx == value:
                box = (j, i, j+d, i+d)
                return self.tileset.crop(box)

    def _save_results(self, image):
        os.mkdir('./results')
        image.save(f"./results/result_sprite.png")

    def generate_sprite_sheet(self):
        matrixes = self._get_map_matrix()
        sprite_width = self.mapdata['tilewidth'] * self.mapdata['width']
        sprite_height = self.mapdata['tilewidth'] * self.mapdata['height']
        sprite = Image.new('RGB', (sprite_width, sprite_height))
        
        for matrix in matrixes:
            x_offset = 0
            y_offset = 0
            for key, value in matrix.items():
                if value != 0:
                    tile = self._get_tile_by_id(value - 1)

                if x_offset == sprite_width:
                    x_offset = 0
                    y_offset += tile.size[1]

                if value != 0:
                    sprite.paste(tile, (x_offset, y_offset), tile)
                x_offset += tile.size[0]
        self._save_results(sprite)
    
    def generate_animated_sprite_sheet(self, frames: int = 4):
        matrixes = self._get_map_matrix()
        sprite_width = self.mapdata['tilewidth'] * self.mapdata['width']
        sprite_height = self.mapdata['tilewidth'] * self.mapdata['height']
        sprite = Image.new('RGB', (sprite_width * frames, sprite_height))
        
        for frame in range(frames):
            for matrix in matrixes:
                x_offset = 0 + (sprite_width * frame)
                y_offset = 0
                for key, value in matrix.items():
                    tile_id = value - 1
                    if value != 0:
                        if "animation" in self.tilemap['tiles'][tile_id]:
                            tile = self._get_tile_by_id(self.tilemap['tiles'][tile_id]['animation'][frame]['tileid'])
                        else:
                            tile = self._get_tile_by_id(tile_id)

                    if x_offset == sprite_width * (frame + 1):
                        x_offset = 0 + (sprite_width * frame)
                        y_offset += tile.size[1]

                    if value != 0:
                        sprite.paste(tile, (x_offset, y_offset), tile)

                    x_offset += tile.size[0]
        self._save_results(sprite)

ExportSprite()

