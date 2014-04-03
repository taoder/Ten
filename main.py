import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, ObjectProperty

app = None

class TenRound(Widget):
    pass


class TenSquare(Widget):
    pass


class TenEmpty(Widget):
    pass


class TenPlaceholder(Widget):
    item = ObjectProperty()

    def __init__(self, **kwargs):
        super(TenPlaceholder, self).__init__()
        print('placeholder')


class TenBoard(Widget):
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)

    def __init__(self, **kwargs):
        super(TenBoard, self).__init__()
        self.board = [[None for x in xrange(3)] for x in xrange(3)]

    def rebuild_background(self):
        self.canvas.before.clear()
        with self.canvas.before:
            csize = self.cube_size, self.cube_size
            for ix, iy in self.iterate_pos():
                TenEmpty(pos=self.index_to_pos(ix, iy), size=csize)

    def reposition(self, *args):
        print('reposition')
        self.rebuild_background()
        # calculate the size of a number
        l = min(self.width, self.height)
        padding = (l / 3.) / 2.5
        cube_size = (l - (padding * 4)) / 3.
        self.cube_size = cube_size
        self.cube_padding = padding

        for ix, iy, square in self.iterate():
            square.size = cube_size, cube_size
            square.pos = self.index_to_pos(ix, iy)

    def iterate(self):
        for ix, iy in self.iterate_pos():
            child = self.board[ix][iy]
            if child:
                yield ix, iy, child

    def iterate_pos(self):
        for ix in range(3):
            for iy in range(3):
                yield ix, iy

    def index_to_pos(self, ix, iy):
        padding = self.cube_padding
        cube_size = self.cube_size
        return [
            (self.x + padding) + ix * (cube_size + padding),
            (self.y + padding) + iy * (cube_size + padding)]


class TenGame(Widget):
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)
    grid = ObjectProperty()

    """board1 = ObjectProperty()
    board2 = ObjectProperty()
    board3 = ObjectProperty()
    board4 = ObjectProperty()
    board5 = ObjectProperty()
    board6 = ObjectProperty()
    board7 = ObjectProperty()
    board8 = ObjectProperty()
    board9 = ObjectProperty()"""

    def __init__(self, **kwargs):
        super(TenGame, self).__init__()

        """self.board = [
            [self.ids.board1.__self__, self.ids.board2.__self__, self.ids.board3.__self__],
            [self.ids.board4.__self__, self.ids.board5.__self__, self.ids.board6.__self__],
            [self.ids.board7.__self__, self.ids.board8.__self__, self.ids.board9.__self__]]"""

    def on_touch_down(self, touch):
        for board in app.ids.grid.__self__.walk(restrict=True):
            if board.collide_with(touch.x, touch.y):
                bsize = board.size
                bpos = board.pos
                self.remove_widget(board)
                self.add_widget(TenSquare(pos=bpos, size=bsize))


class TenApp(App):
    def build(self):
        global app
        app = self
        return TenGame()

if __name__ == '__main__':
    TenApp().run()