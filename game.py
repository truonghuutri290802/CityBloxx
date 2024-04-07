import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
win = pygame.display.set_mode((400, 640))
pygame.display.set_caption("City Bloxx | Abthahi & Programming")

# Load images
base = pygame.image.load("img/base.png")
block = pygame.image.load("img/block.png")
sign = pygame.image.load("img/sign.png")
wall = pygame.image.load("img/wall.png")
block_icon = pygame.image.load("img/block-icon.png")
balloon = pygame.image.load("img/balloon.png")

# Load font
font = pygame.font.Font("poppins.ttf", 16)

# Define colors
WHITE = (255, 255, 255)
BLUE = (33, 158, 188)
ORANGE = (251, 133, 0)
GREEN = (43, 147, 72)
GRAY = (200, 200, 200)
DARK_BLUE = (2, 48, 71)

# Class for blocks
class Block:
    def __init__(self, x, y, base):
        self.bx = x
        self.by = y
        self.bay = 0.4
        self.bvy = 0
        self.base = base

    def anchor(self, x, y):
        self.bx = x
        self.by = y

    def drop(self):
        self.bvy += self.bay
        self.by += self.bvy

    def collide_with_block(self, block):
        if self.bx <= block.bx + 64 and self.bx + 64 >= block.bx:
            if self.by + 64 >= block.by:
                self.by = block.by - 64
                self.bvy = 0
                self.bay = 0
                return True
        return False

    def collide_with_ground(self, camera):
        if self.by + 64 >= (520 + camera):
            self.bvy = 0
            self.bay = 0
            self.by = (520 + camera) - 64
            return True
        return False

    def move_camera(self, cm):
        self.by += cm

    def draw(self):
        if self.base == 1:
            win.blit(base, (self.bx - 32, self.by))
        else:
            win.blit(block, (self.bx - 32, self.by))

# Function to draw text
def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    win.blit(text_surface, (x, y))

# Main function
def main():
    is_running = True
    t = 0
    cx = 320
    cy = 100
    blocks = [Block(cx, cy, 1)]
    angle = 1
    angleA = 0
    angleV = 0
    gravity = 0.0004
    base = 1
    current = 0
    camera = 0
    dropping = False
    balloonx = -100

    clock = pygame.time.Clock()

    while is_running:
        win.fill(BLUE)

        # Rope
        force = gravity * math.sin(angle)
        angleA = force * -1
        angleV += angleA
        angle += angleV
        cx = 130 * math.sin(angle) + 200
        cy = 130 * math.cos(angle)
        blocks[current].anchor(cx, cy)

        if blocks[0].collide_with_ground(camera):
            if len(blocks) <= 2:
                dropping = False
        if base == 0:
            blocks[0].drop()

        for i in range(1, len(blocks) - 1):
            if i > 0:
                if blocks[i].collide_with_block(blocks[i - 1]):
                    dropping = False
            blocks[i].drop()

            if blocks[i].collide_with_ground(camera):
                blocks.pop(i)
                current = len(blocks) - 1
                dropping = False
                if len(blocks) >= 4:
                    camera -= 64

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not dropping:
                        if len(blocks) >= 4:
                            camera += 64
                            for i in range(len(blocks) - 1):
                                blocks[i].move_camera(64)
                        blocks.append(Block(cx, cy, 0))
                        current = len(blocks) - 1
                        base = 0
                        dropping = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dropping:
                    if len(blocks) >= 4:
                        camera += 64
                        for i in range(len(blocks) - 1):
                            blocks[i].move_camera(64)
                    blocks.append(Block(cx, cy, 0))
                    current = len(blocks) - 1
                    base = 0
                    dropping = True

        if len(blocks) >= 12:
            balloonx += 0.2

        # Rendering Part
        win.blit(balloon, (balloonx, (100 + camera) - 768))
        pygame.draw.rect(win, GREEN, (0, 540 + camera, 400, 100))
        win.blit(wall, (0, 540 + camera - 118))
        pygame.draw.rect(win, GRAY, (20, 520 + camera, 360, 20))
        pygame.draw.line(win, DARK_BLUE, (200, 0), (cx, cy), 2)

        for blk in blocks:
            blk.draw()

        win.blit(sign, (260, 640 + camera - 157))
        win.blit(block_icon, (10, 10))
        draw_text(str(len(blocks) - 1), 32, 8)

        pygame.display.update()
        clock.tick(60)
        t += 1

    pygame.quit()

if __name__ == "__main__":
    main()
