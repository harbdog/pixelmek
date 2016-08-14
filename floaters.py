import board
import cocos


class TextFloater(cocos.text.Label):

    def __init__(self, text, color=(255, 255, 255, 255), font_size=(2*board.Board.TILE_SIZE)//4):
        super(TextFloater, self).__init__(text, color=color, font_size=font_size,
                                          anchor_x='center', font_name='Convoy')
