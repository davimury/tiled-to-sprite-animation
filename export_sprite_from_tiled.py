import lua_imports; lua_imports.lua_importer.register()
from itertools import product
from PIL import Image
import tilemap
import mapdata

class ExportSprite:
    def __init__(self) -> None:
        self.tilemap = {}
        self.tilemap = self._transform_lua_table_to_dict(tilemap.lua_module[0])
        self.mapdata = self._transform_lua_table_to_dict(mapdata.lua_module[0])
        self.matrix = self._get_map_matrix()
        self.sprite = Image.open(self.tilemap['image'])
        self.generate_sprite_sheet(1600,1600)

    def _transform_lua_table_to_dict(self, object):
        tmp = {}
        for key, value in dict(object).items():
            if not isinstance(value, str) and not isinstance(value, int):
                value = self._transform_lua_table_to_dict(value)
            tmp[key] = value
        return tmp
    
    def _get_map_matrix(self):
        matrix = {}
        for key, value in self.mapdata['layers'].items():
            for data_key, data_value in value['data'].items():
                if data_value != 0:
                    matrix[data_key] = data_value
        return matrix

    def _get_tile_by_id(self, value):
        w, h = self.sprite.size
        d = 16 # Tamanho
        for idx, (i, j) in enumerate(product(range(0, h-h%d, d), range(0, w-w%d, d))):
            if idx == value:
                box = (j, i, j+d, i+d)
                return self.sprite.crop(box)
        
    def generate_sprite_sheet(self, width, height):
        matrix = self._get_map_matrix()
        sprite = Image.new('RGB', (width, height))
        x_offset = 0
        y_offset = 0

        for key, value in matrix.items():
            tile = self._get_tile_by_id(value - 1)
            if x_offset == width:
                x_offset = 0
                y_offset += tile.size[1]
            sprite.paste(tile, (x_offset, y_offset))
            x_offset += tile.size[0]
        sprite.show()
        return sprite

ExportSprite()

