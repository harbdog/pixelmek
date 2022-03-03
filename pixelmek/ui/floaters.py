import cocos


class TextFloater(cocos.text.Label):

    def __init__(self, text, color=(255, 255, 255, 255), font_size=None,
                 font_name='Convoy', anchor_x='center', anchor_y='center'):

        if font_size is None:
            from pixelmek.ui.board import Board
            font_size = Board.TILE_SIZE // 2

        super(TextFloater, self).__init__(text, color=color, font_size=font_size, font_name=font_name,
                                          anchor_x=anchor_x, anchor_y=anchor_y)

    def set_text(self, text):
        self.element.text = text
