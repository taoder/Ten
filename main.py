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
    scale = NumericProperty(1)


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
        self.bind(pos=self.relayout, size=self.relayout)
        self.cells = []
        self.animations = []

        for index in range(9):
            cell = TenEmpty(index=index)
            self.add_widget(cell)
            self.cells.append(cell)
        self.relayout()

    def relayout(self, *args):
        xmin, ymin, cs, s, padding = self.cube_info
        x = xmin
        y = ymin

        for index, cell in enumerate(self.cells):
            cell.pos = x, y
            cell.scale = cs
            if index % 3 == 2:
                x = xmin
                y += cs + padding
            else:
                x += cs + padding

    @property
    def cube_info(self):
        s = min(self.width, self.height)

        padding = (s / 3.) / 12
        cs = (s - (padding * 4)) / 3.
        xmin = self.x + padding
        ymin = self.y + padding
        return xmin, ymin, cs, s, padding

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
        xmin, ymin, cs, s, padding = self.cube_info
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
                y += cs + padding
            else:
                x += cs + padding

    @property
    def cube_info(self):
        s = min(self.width, self.height)

        padding = (s / 3.) / 12
        cs = (s - (padding * 4)) / 3.
        xmin = self.x + (self.width - s) / 2. + padding
        ymin = self.y + (self.height - s) / 2. + padding
        return xmin, ymin, cs, s, padding

    @property
    def cube_info_focus(self):

        index = self.board_focused_index

        xmin, ymin, cs, side, padding = self.cube_info
        t = math.ceil(((index / 3.) / -2.) * 2.) / 2.
        x = xmin + ((index % 3) + (index % 3) / -2.) * (cs + padding)
        y = ymin + (int(index / 3) + t) * (cs + padding)
        cs_board_focused = side/1.5 - 2 * padding


        xn = 1
        yn = 1
        size_index_x = 0
        size_index_y = 0
        if index == 0 or index == 1 or index == 2:
            size_index_y = cs_board_focused
        if index == 0 or index == 3 or index == 6:
            size_index_x = cs_board_focused
        if index == 2 or index == 5 or index == 8:
            xn = -1
        if index == 6 or index == 7 or index == 8:
            yn = -1

        _xmin = x + xn * ((index % 3) / 4. * cs_board_focused) + size_index_x
        _ymin = y + yn * (math.floor(index / 3.) / 4. * cs_board_focused) + size_index_y
        _side = side * 1 / 3
        _padding = (_side / 3.) / 12
        _cs = (_side - (_padding * 4)) / 3.
        return x, y, cs_board_focused, _xmin, _ymin, _cs, _padding

    @property
    def cube_info_focus_milieu(self):


        xmin, ymin, cs, side, padding = self.cube_info
        t = math.ceil(((1 / 3.) / -2.) * 2.) / 2.
        x = xmin + ((1 % 3) + (1 % 3) / -2.) * (cs + padding)
        y = ymin + (int(1 / 3) + t) * (cs + padding)
        cs_board_focused = side/1.5 - 2 * padding

        _xmin = x + (1 / 4. * cs_board_focused)
        _ymin = y + cs_board_focused
        _side = side * 1 / 3
        _padding = (_side / 3.) / 12
        _cs = (_side - (_padding * 4)) / 3.
        return x, y, cs_board_focused, _xmin, _ymin, _cs, _padding

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

        if index == 4:
            x, y, cs_board_focus, _xmin, _ymin, _cs, _padding = self.cube_info_focus_milieu
        else:
            x, y, cs_board_focus, _xmin, _ymin, _cs, _padding = self.cube_info_focus

        self.stop_animations()
        self.animate(board, x=x, y=y, size=(cs_board_focus, cs_board_focus))

        _x = _xmin
        _y = _ymin

        for _index, _board in enumerate(self.boards):
            if board is _board:
                if _index % 3 == 2:
                    _x = _xmin
                    _y += _cs + _padding
                else:
                    _x += _cs + _padding
                continue
            self.animate(_board, x=_x, y=_y, size=(_cs,_cs))
            if _index % 3 == 2:
                _x = _xmin
                _y += _cs + _padding
            else:
                _x += _cs + _padding

    def unfocus(self):
        index = self.board_focused_index
        if index == -1:
            return
        board = self.board_focused
        xmin, ymin, cs, side, padding = self.cube_info
        x = xmin + (index % 3) * (cs + padding)
        y = ymin + int(index / 3) * (cs + padding)

        self.stop_animations()
        self.animate(self.board_focused,
                x=x, y=y, size=(cs, cs))
        self.relayout()

        self.board_focused_index = -1

    def stop_animations(self):
        while self.animations:
            anim, widget = self.animations.pop()
            anim.stop_all(widget)

    def animate(self, widget, **kwargs):
        kwargs['d'] = .50
        kwargs['t'] = 'out_quart'
        anim = Animation(**kwargs)
        anim.start(widget)
        self.animations.append((anim, widget))
        return anim



if __name__ == '__main__':
    class TenApp(App):
        def build(self):
            return TenBoardLayout()
    TenApp().run()
