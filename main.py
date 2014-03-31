import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty


class TenPartOfBoard(Widget):
    pass


class TenSquare(TenPartOfBoard):
    pass




class TenGame(Widget):
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)

    def __init__(self, **kwargs):
        super(TenGame, self).__init__()

        self.board = [[None for x in xrange(3)] for x in xrange(3)]

    def rebuild_background(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0)
            Rectangle(pos=self.pos, size=self.size)
            Color(1, 0, 0)
            csize = self.cube_size, self.cube_size
            for ix, iy in self.iterate_pos():
                Rectangle(pos=self.index_to_pos(ix, iy), size=csize)

    def reposition(self, *args):
        print("reposition")
        self.rebuild_background()
        # calculate the size of a number
        l = min(self.width, self.height)
        padding = (l / 3.) / 12.
        cube_size = (l - (padding * 4)) / 3.
        self.cube_size = cube_size
        self.cube_padding = padding

        for ix, iy, board in self.iterate():
            print("ici")
            board.size = cube_size, cube_size
            board.pos = self.index_to_pos(ix, iy)

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


class TenApp(App):
    def build(self):
        print("build TenApp")
        game = TenGame()
        game.reposition()
        game.reposition()
        return game


if __name__ == '__main__':
    TenApp().run()