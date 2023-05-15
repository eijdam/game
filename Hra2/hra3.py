import pygame as pg
from PIL import Image, ImageSequence

pg.init()

screen = pg.display.set_mode((1920, 1080), pg.RESIZABLE)
pg.display.set_caption("Game")
font1 = pg.font.Font("fonts/vhs.ttf", 35)
pg.mouse.set_visible(False)
# Define the cursor radius and the color of the glow
CURSOR_RADIUS = 10
GLOW_COLOR = (255, 255, 255)
GLOW_ALPHA = 0


class Button:
    def __init__(self, x_pos, y_pos, text, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled

    def draw(self):
        button_text = font1.render(self.text, True, (255, 255, 255))
        button_rect = pg.rect.Rect((self.x_pos, self.y_pos), (300, 40))  # velkost tlacitok -adam
        if self.enabled:
            if self.check_click():
                pg.draw.rect(screen, (169, 169, 169), button_rect, 0, 5)
            else:
                pg.draw.rect(screen, (128, 128, 128), button_rect, 0, 5)
        else:
            pg.draw.rect(screen, (0, 0, 0), button_rect, 0, 5)
            pg.draw.rect(screen, (0, 0, 0), button_rect, 2, 5)
        screen.blit(button_text, (self.x_pos + 3, self.y_pos + 3))

    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        button_rect = pg.rect.Rect((self.x_pos, self.y_pos), (300, 40))  # velkost tlacitok -adam
        if left_click and button_rect.collidepoint(mouse_pos):
            return True
        return False


def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        frame = frame.resize((1920, 1080), resample=Image.BOX)  # Resize the frame
        pygameImage = pg.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
    return frames


class AnimatedSpriteObject(pg.sprite.Sprite):
    def __init__(self, x, y, frames, animation_speed):
        super().__init__()
        self.frames = frames
        self.image_index = 0
        self.image = self.frames[self.image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = animation_speed
        self.last_update_time = pg.time.get_ticks()

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed * 1000:
            self.image_index = (self.image_index + 1) % len(self.frames)
            self.image = self.frames[self.image_index]
            self.last_update_time = current_time

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


play_button = Button(820, 500, "PLAY", True)
quit_button = Button(820, 570, "QUIT", True)

frames = loadGIF("videos/VHSvideo.gif")
background = AnimatedSpriteObject(960, 540, frames, 0.1)

clock = pg.time.Clock()


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            screen.fill((0, 0, 0))
    background.update()
    background.draw()

    play_button.draw()
    if play_button.check_click():
        print("Play button clicked")

    quit_button.draw()
    if quit_button.check_click():
        running = False

    # Draw cursor with glow effect
    mouse_pos = pg.mouse.get_pos()
    cursor = pg.Surface((CURSOR_RADIUS*2, CURSOR_RADIUS*2), pg.SRCALPHA)
    pg.draw.circle(cursor, GLOW_COLOR + (GLOW_ALPHA,), (CURSOR_RADIUS, CURSOR_RADIUS), CURSOR_RADIUS)
    screen.blit(cursor, (mouse_pos[0]-CURSOR_RADIUS, mouse_pos[1]-CURSOR_RADIUS))
    pg.draw.circle(screen, GLOW_COLOR, mouse_pos, CURSOR_RADIUS, 0)

    pg.display.update()
    clock.tick(60)

pg.quit()





# Load the GIF frames


##adam kup zajtra ryzu 5/14/2023
       



