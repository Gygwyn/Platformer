import arcade
import os
from Player import Player

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Coiner"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class Spel(arcade.View):



    def __init__(self):

        

        super().__init__()

        filepath = os.path.abspath(__file__)
        dirpath = os.path.dirname(filepath)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        self.player = Player()

        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0
        
        self.score = 0

        # Ladda ljud
        self.collect_coin_sound = arcade.load_sound(dirpath +"/ljud/Coinsound.wav")
        self.jump_sound = arcade.load_sound(dirpath +"/ljud/Jumpsound.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        
        filepath = os.path.abspath(__file__)
        dirpath = os.path.dirname(filepath)

        self.view_bottom = 0
        self.view_left = 0
        
        self.score = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        
        self.player_list.append(self.player.sprite)

        # Skapa marken
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Positioner där lådorna ska vara
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Lådor på marken
            wall = arcade.Sprite(dirpath +"/bilder/PNG/Tiles/boxCrate_single.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(dirpath +"/bilder/PNG/Items/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player.sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        self.player.setup(self.physics_engine)

    def on_draw(self):
        """ Rendera skärmen """

        arcade.start_render()
        # return
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):

        self.player.on_key_press(key, modifiers)


    def on_key_release(self, key, modifiers):

        self.player.on_key_release(key, modifiers)


    def on_update(self, delta_time):
        """ Rörelse och spel logistik """

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player.sprite, self.coin_list)
        for coin in coin_hit_list:
            # Ta bort myntet
            coin.remove_from_sprite_lists()
            # Ljud för myntet
            arcade.play_sound(self.collect_coin_sound)
            # Score 
            self.score += 1

        changed = False

        # Skrolla vänster
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player.sprite.left
            changed = True

        # Skrolla höger
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.sprite.right > right_boundary:
            self.view_left += self.player.sprite.right - right_boundary
            changed = True

        # Skrolla upp
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.sprite.top > top_boundary:
            self.view_bottom += self.player.sprite.top - top_boundary
            changed = True

        # Skrolla ner
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.sprite.bottom
            changed = True

        if changed:

            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)