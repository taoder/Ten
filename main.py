import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty, ObjectProperty


class TenRound(Widget):
    pass


class TenSquare(Widget):
    pass


class TenEmpty(Widget):
    pass


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
        self.rebuild_background()
        # calculate the size of a number
        l = min(self.width, self.height)
        padding = (l / 3.) / 6.
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
    board1 = ObjectProperty()
    board2 = ObjectProperty()
    board3 = ObjectProperty()
    board4 = ObjectProperty()
    board5 = ObjectProperty()
    board6 = ObjectProperty()
    board7 = ObjectProperty()
    board8 = ObjectProperty()
    board9 = ObjectProperty()

    def __init__(self, **kwargs):
        super(TenGame, self).__init__()

        self.board = [
            [self.board1, self.board2, self.board3],
            [self.board4, self.board5, self.board6],
            [self.board7, self.board8, self.board9]]

    def on_touch_move(self, touch):
        print("ici")
        bsize = self.board1.size
        bpos = self.board1.pos
        self.board1 = TenSquare(pos=bpos, size=bsize)


class TenApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    TenApp().run()