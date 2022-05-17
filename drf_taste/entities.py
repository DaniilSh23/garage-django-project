class Item:
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def to_dict(self):
        '''
        Функция для превращения атрибутов класса в словарь.
        Была нужна для "костыльного" примера.
        '''
        return {
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
        }