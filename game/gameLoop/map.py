import pygame, os


class Map:
    def __init__(self, file, spriteMap) -> None:
        self.file = file
        self.respawnPoint = (0, 0)
        self.spriteSheet = SpriteSheet(spriteMap)
        self.colliders = []
        self.decorative = []
        self.hazardous = []
        self.renderedImage = None
        self.loadMap(self.file)
        self.render()

    def loadMap(self, file):
        # map is defined as a grid of tiles
        # Each tile has a number which tells the game what it is
        # 0 = empty space
        # 1 = basic tile with top left wall
        # 2 = basic tile with top wall
        # 3 = basic tile with top right wall
        # 4 = basic tile with left wall
        # 5 = basic tile with middle wall
        # 6 = basic tile with right wall
        # 7 = basic tile with bottom left wall
        # 8 = basic tile with bottom wall
        # 9 = basic tile with bottom right wall
        # 10 = special wall with top wall
        # 11 = special wall with top wall
        # 12 = special wall with top wall
        # 13 = special wall with lincoln poster 1
        # 14 = special wall with small nuclear poster
        # 15 = special wall with big nuclear poster 1
        # 16 = special wall with middle wall
        # 17 = special wall with middle wall
        # 18 = special wall with middle wall
        # 19 = special wall with lincoln poster 1
        # 20 = special wall with middle wall
        # 21 = special wall with big nuclear poster 2
        # 22 = skyscraper wall left
        # 23 = skyscraper wall left
        # 24 = skyscraper wall left
        # 25 = skyscraper wall midle
        # 26 = skyscraper wall midle
        # 27 = skyscraper wall midle
        # 28 = skyscraper wall right
        # 29 = skyscraper wall right
        # 30 = skyscraper wall right
        # 31 = level label
        # 32-33-34 - water puddle
        tileInSpriteMap = {0: [0, 0],
                           1: [32, 0], 2: [64, 0], 3: [96, 0], 4: [32, 32], 5: [64, 32], 6: [96, 32],
                           7: [32, 64], 8: [64, 64], 9: [96, 64], 10: [32, 128], 11: [64, 128], 12: [96, 128],
                           13: [128, 128], 14: [160, 128], 15: [192, 128], 16: [32, 160], 17: [64, 160],
                           18: [96, 160], 19: [128, 160], 20: [160, 160], 21: [192, 160],
                           22: [160, 0], 23: [160, 32], 24: [160, 64], 25: [224, 0], 26: [224, 32], 27: [224, 64],
                           28: [192, 0], 29: [192, 32], 30: [192, 64], 31: [544, 0], 32: [448, 512], 33: [480, 512], 34: [512, 512]}
        with open(file, "r") as f:
            data = f.readline().split(";")
            self.screenY = int(data[0])
            self.screenX = int(data[1])
            self.respawnPoint = (int(data[2]), int(data[3]))
            self.renderedImage = pygame.Surface(
                (self.screenX*2, self.screenY*2), pygame.SRCALPHA, 32).convert_alpha()
            for y, line in enumerate(f.readlines()):
                for x, symbols in enumerate(line.split()):
                    if "|" in symbols:
                        for symbol in symbols.split("|"):
                            if int(symbol) < 0:
                                pass
                            else:
                                if int(symbol) in [0]:
                                    self.decorative.append(
                                        Tile(tileInSpriteMap[int(symbol)], x*64, y*64, self.spriteSheet))
                                elif int(symbol) in [32, 33, 34]:
                                    self.hazardous.append(
                                        Tile(tileInSpriteMap[int(symbol)], x*64, y*64, self.spriteSheet))
                                else:
                                    self.colliders.append(
                                        Tile(tileInSpriteMap[int(symbol)], x*64, y*64, self.spriteSheet))
                    else:
                        if int(symbols) < 0:
                            pass
                        else:
                            if int(symbols) in [0]:
                                self.decorative.append(
                                    Tile(tileInSpriteMap[int(symbols)], x*64, y*64, self.spriteSheet))
                            elif int(symbols) in [32, 33, 34]:
                                self.hazardous.append(
                                    Tile(tileInSpriteMap[int(symbols)], x*64, y*64, self.spriteSheet))
                            else:
                                self.colliders.append(
                                    Tile(tileInSpriteMap[int(symbols)], x*64, y*64, self.spriteSheet))

    def render(self):
        for tile in self.colliders:
            tile.draw(self.renderedImage)
        for tile in self.decorative:
            tile.draw(self.renderedImage)
        for tile in self.hazardous:
            tile.draw(self.renderedImage)

    def getMap(self):
        return self.renderedImage

    def scale(self, scale):
        return pygame.transform.scale(self.renderedImage, (int(self.screenX * scale), int(self.screenY * scale)))

    def scaledToHeight(self, height):
        return pygame.transform.scale(self.renderedImage, (int(self.screenX * height/self.screenY), height))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tileType, x: int, y: int, spritesheet) -> None:
        self.tileType = tileType
        self.x = x
        self.y = y
        self.spriteSheet = spritesheet
        self.loadTexture(tileType)
        self.rect = pygame.Rect(x, y, 64, 64)

    def draw(self, surface):
        surface.blit(pygame.transform.scale(
            self.image, (64, 64)), (self.x, self.y))

    def loadTexture(self, tileType):
        self.image = self.spriteSheet.getSprite(tileType)


class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y):
        sprite = pygame.Surface((32, 32))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return sprite

    def getSprite(self, spriteData):
        x, y = spriteData
        image = self.get_sprite(x, y)
        return image


if __name__ == '__main__':
    pygame.init()
    # screen = pygame.display.set_mode((20*32, 4*32))
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    dirname = os.path.dirname(__file__)
    testmap = os.path.join(dirname, 'testmap.mp')
    titlemap = os.path.join(dirname, '../assets/Tiles/tilemap.png')
    map = Map(testmap, titlemap)
    mapX = 0
    mapY = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mapX += 16
                elif event.key == pygame.K_RIGHT:
                    mapX -= 16
                elif event.key == pygame.K_UP:
                    mapY += 16
                elif event.key == pygame.K_DOWN:
                    mapY -= 16
        screen.fill((80, 80, 0))
        # map.map[2][1].draw(screen)
        # screen.blit(map.spriteSheet.get_sprite(32, 0, 32, 32), (32, 0))
        mapImg = map.scaledToHeight(600)
        # mapImg = pygame.transform.scale(mapImg, (800, 600))
        screen.blit(mapImg, (mapX, mapY))

        pygame.display.flip()
        clock.tick(60)
