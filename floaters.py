import board
import cocos


class TextFloater(cocos.text.Label):

    def __init__(self, text, color=(255, 255, 255, 255), font_size=(2*board.Board.TILE_SIZE)//4,
                 anchor_x='center', anchor_y='center'):
        super(TextFloater, self).__init__(text, color=color, font_size=font_size, font_name='Convoy',
                                          anchor_x=anchor_x, anchor_y=anchor_y)