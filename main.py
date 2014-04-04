import kivy
kivy.require('1.8.0')

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics import *
from kivy.animation import Animation
import math


class TenEmpty(Widget):
    index = NumericProperty(0)
    #scale = NumericProperty(1)
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)


class TenRound(Widget):
    pass


class TenSquare(Widget):
    pass


class TenBoard(Widget):
    index = NumericProperty(0)
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)

    def __init__(self, **kwargs):
        super(TenBoard, self).__init__(**kwargs)
        self.cells = [self.ids.cell1, self.ids.cell2, self.ids.cell3,
                      self.ids.cell4, self.ids.cell5, self.ids.cell6,
                      self.ids.cell7, self.ids.cell8, self.ids.cell9]
        self.relayout()

    def relayout(self, *args):
        xmin, ymin, cs, _ = self.cube_info
        x = xmin
        y = ymin

        for index, cell in enumerate(self.cells):
            cell.pos = x, y
            cell.scale = cs
            if index % 3 == 2:
                x = xmin
                y += cs
            else:
                x += cs

    @property
    def cube_info(self):
        s = min(self.width, self.height)
        cs = s / 3
        xmin = self.x + (self.width - s) / 2.
        ymin = self.y + (self.height - s) / 2.
        return xmin, ymin, cs, s

    """def collide_point(self, x, y):
        x = (x - self.x) / self.scale
        y = (y - self.y) / self.scale
        x += self.x
        y += self.y
        return super(TenBoard, self).collide_point(x, y)"""

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.parent.board_focused_index == self.index :
            self.parent.unfocus()
        else:
            self.parent.unfocus()
            self.parent.focus(self.index)
        return True


class TenBoardLayout(Widget):

    board_focused_index = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(TenBoardLayout, self).__init__(**kwargs)
        self.bind(pos=self.relayout, size=self.relayout)
        self.boards = []
        self.animations = []
        for index in range(9):
            board = TenBoard(index=index)
            self.add_widget(board)
            self.boards.append(board)
        self.relayout()

    def relayout(self, *args):
        xmin, ymin, cs, _ = self.cube_info
        x = xmin
        y = ymin
        cube_size = cs, cs

        for index, board in enumerate(self.boards):
            if index == self.board_focused_index:
                board.pos = xmin, ymin
                board.size = cube_size
            else:
                board.pos = x, y
                board.size = cube_size
            if index % 3 == 2:
                x = xmin
                y += cs
            else:
                x += cs

    @property
    def cube_info(self):
        s = min(self.width, self.height)
        cs = s / 3
        xmin = self.x + (self.width - s) / 2.
        ymin = self.y + (self.height - s) / 2.
        return xmin, ymin, cs, s

    @property
    def board_focused(self):
        if self.board_focused_index == -1:
            return None
        return self.boards[self.board_focused_index]

    def focus(self, index):
        self.board_focused_index = index
        board = self.board_focused
        self.remove_widget(board)
        self.add_widget(board)
        xmin, ymin, cs, side = self.cube_info
        t = math.ceil(((index / 3.) / -2.) * 2.) / 2.
        x = xmin + ((index % 3) + (index % 3) / -2.) * cs
        y = ymin + (int(index / 3) + t) * cs
        self.stop_animations()
        self.animate(board, x=x, y=y, size=(side/1.5, side/1.5))
        for _board in self.boards:
            if board is _board:
                continue
            self.animate(_board)

    def unfocus(self):
        index = self.board_focused_index
        if index == -1:
            return
        board = self.board_focused
        xmin, ymin, cs, side = self.cube_info
        x = xmin + (index % 3) * cs
        y = ymin + int(index / 3) * cs

        self.stop_animations()
        self.animate(self.board_focused,
                x=x, y=y, size=(cs, cs))
        for _board in self.boards:
            if board is _board:
                continue
            self.animate(_board)

        self.board_focused_index = -1

    def stop_animations(self):
        while self.animations:
            anim, widget = self.animations.pop()
            anim.stop_all(widget)

    def animate(self, widget, **kwargs):
        kwargs['d'] = .25
        #kwargs['t'] = 'out_quart'
        anim = Animation(**kwargs)
        anim.start(widget)
        self.animations.append((anim, widget))
        return anim



if __name__ == '__main__':
    class TenApp(App):
        def build(self):
            return TenBoardLayout()
    TenApp().run()
