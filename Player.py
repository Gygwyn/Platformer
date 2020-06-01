import arcade
import os

# Konstanter
CHARACTER_SCALING = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20


class Player:


    def __init__(self):
        
        filepath = os.path.abspath(__file__)
        dirpath = os.path.dirname(filepath)

        self.sprite = None
        self.jump_sound = arcade.load_sound(dirpath +"/ljud/Jumpsound.wav")

        # Spelar inställningar, vart spelaren står på spelet.
        image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        self.sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.sprite.center_x = 64
        self.sprite.center_y = 96
        

    def setup(self, physics_engine):
        
        self.physics_engine = physics_engine

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.sprite.change_x = 0
