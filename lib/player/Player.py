import sys, pygame, os, math
try:
    import simplegui
except ImportError:
    sys.argv.append('--no-controlpanel')
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from lib.player.interactions.keyboard import Keyboard
from lib.player.interactions.player_move import PlayerMove
from lib.player.interactions.change_slot import ChangeSlot
from lib.player.inventory import Inventory


class Player:

    def __init__(self, x_pos, y_pos, lives, inventory):
        self.inven = inventory
        self.x = x_pos
        self.y = y_pos
        self.pos = (x_pos, y_pos)
        self.max_health = 100
        self.health = self.max_health
        self.lives = lives
        self.dead = False
        self.game_over = False
        self.is_moving = False
        self.mouse_pos = pygame.mouse.get_pos()
        x = os.path.join(os.path.dirname(__file__), "../../textures/sprite_sheets/player/playersprite.png")
        self.img = simplegui._load_local_image(x)
        # self.img = pygame.image.load(x).convert_alpha()
        self.height = 180
        self.width = 411
        self.frame_width = self.width / 3
        self.frame_centre = self.frame_width / 2
        self.frame_index = 0
        self.frame_up = True
        self.clock = 0
        self.rot = 0
        self.speed = 5  # amount of frames per sprite update

    def draw(self, canvas):
        canvas.draw_image(self.img, (self.frame_width * self.frame_index + self.frame_centre, self.height / 2),
                          (self.frame_width, self.height), self.pos, (50, 50), self.rot)
        self.inven.draw(canvas)

    def update(self):
        self.inven.update()
        self.update_rot()
        self.clock += 1
        if self.clock % self.speed == 0:
            self.update_sprite()

    def update_rot(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if self.mouse_pos[0] > self.x and self.mouse_pos[1] > self.y:
            self.rot = -(math.pi + math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2))))
        if self.mouse_pos[0] > self.x and self.mouse_pos[1] < self.y:
            self.rot = math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2)))
        if self.mouse_pos[0] < self.x and self.mouse_pos[1] < self.y:
            self.rot = math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2)))
        if self.mouse_pos[0] < self.x and self.mouse_pos[1] > self.y:
            self.rot = -(math.pi + math.asin(
                (self.mouse_pos[0] - self.x) / math.sqrt(math.pow(self.mouse_pos[0] - self. x, 2) +
                                                         math.pow(self.mouse_pos[1] - self.y, 2))))

    def update_sprite(self):
        if self.is_moving:
            if self.frame_up:
                self.frame_index += 1
                if self.frame_index == 3:
                    self.frame_up = False
            if not self.frame_up:
                self.frame_index -= 1
                if self.frame_index == 0:
                    self.frame_up = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
        if self.lives == 0:
            self.game_over = True


if __name__ == '__main__':
    CANVASWIDTH = 1000
    CANVASHEIGHT = 750
    inven = Inventory(3, 100, CANVASWIDTH, CANVASHEIGHT)
    player = Player(CANVASWIDTH / 2, CANVASHEIGHT / 2, 3, inven)
    kbd = Keyboard()
    player_move = PlayerMove(player, kbd)
    change_slot = ChangeSlot(inven, kbd)

    def draw(canvas):
        player_move.update()
        change_slot.update()
        player.update()
        player.draw(canvas)

    frame = simplegui.create_frame("Game", CANVASWIDTH, CANVASHEIGHT)
    frame.set_canvas_background('Grey')
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(kbd.key_down)
    frame.set_keyup_handler(kbd.key_up)
    frame.start()
