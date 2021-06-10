import json

from domain import NumpyArrayEncoder

class imageObjectJson:
    def __init__(self, name, data, width, height, array):
        self.name = name
        self.data = data
        self.width = width
        self.height = height
        self.array = array


    def toJson(self):

        return {"nome_arquivo": self.name,
                "data": self.data,
                "width": self.width,
                "height": self.height,
                "image_normalizada": str(json.dumps(self.array, cls=NumpyArrayEncoder.NumpyArrayEncode))}

