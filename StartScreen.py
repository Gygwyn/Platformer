import arcade
from Spel import Spel


# Konstanter
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

class StartScreen(arcade.View):
    
    def __init__(self):
        super().__init__()


    def on_draw(self):
        """ Rita viewen """
        arcade.start_render()
        super().on_draw()
        arcade.draw_text("Coinerman", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to begin the journey, ZERG", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Om användaren trycker på musknappen, starta spelet. """
        game_view = Spel()
        game_view.setup()
        self.window.show_view(game_view)
