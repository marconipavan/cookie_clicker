from math import ceil

class UpgradeSingleton:
    _instance = None

    _upgrades = []
    _count = 0

    produtos = {
        # name : [CookiesPorSecond (cps), custo, unidades compradas]
        'product0': [0.1, 15, 0],
        'product1': [1, 100, 0],
        'product2': [8, 1100, 0],
        'product3': [47, 12000, 0],
        'product4': [260, 130000, 0],
        'product5': [1400, 1, 0],
        'product6': [7800, 1, 0],
        'product7': [4400, 1, 0],
        'product8': [260000, 1, 0],
        'product9': [1, 1, 0],
        'product10': [1, 1, 0],
        'product11': [1, 1, 0],
        'product12': [1, 1, 0],
        'product13': [1, 1, 0],
        'product14': [1, 1, 0],
        'product15': [1, 1, 0],
        'product16': [1, 1, 0],
        'product17': [1, 1, 0],
        'product18': [1, 1, 0],
        'product19': [1, 1, 0],
        'blank': [1, 1, 0]
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def upgrade_next(self):
        if self._count < len(self._upgrades):
            up = self._upgrades[self._count]
            self.produtos[up.product][0] *= up.multplicador
            self._count += 1

    def count_product(self, product: int):
        self.produtos[product][2] += 1
    
    def update_cost(self, product: str):
        self.produtos[product][1] = ceil(self.produtos[product][1] * 1.15)

    def buy(self, product: str):
        self.count_product(product)
        self.update_cost(product)

class Upgrade:
    def __init__(self, product: str, multplicador: int=1):
        self.product = product
        self.multplicador = multplicador
        UpgradeSingleton()._upgrades.append(self)

Upgrade('product0', 2)
Upgrade('product0', 2)
Upgrade('product1', 2)
Upgrade('product1', 2)
Upgrade('product0', 2)
Upgrade('product2', 2)
# A partir daqui, o css coloca um raios de ::before na tag e estraga tudo
#Upgrade('blank')
#Upgrade('product2', 2)
#Upgrade('product3', 2)
#Upgrade('blank')
