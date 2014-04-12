__version__ = '0.1.0'
import kivy
kivy.require('1.8.0')

from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.animation import Animation
import math
import time


div_padding_board = 5
div_padding_cell = 2


class TenCell(Widget):
    index = NumericProperty(0)
    scale = NumericProperty(0)
    empty = NumericProperty(1)
    circle = NumericProperty(0)
    square = NumericProperty(0)

    @property
    def value(self):
        if self.empty == 1:
            return "empty"
        else:
            if self.circle == 1:
                return "circle"
            else:
                return "square"

    def collide_point(self, x, y):
        x = (x - self.parent.x) / self.parent.scale
        y = (y - self.parent.y) / self.parent.scale
        if self.x <= x <= (self.x + self.width) and self.y <= y <= (self.y + self.height):
            return True
        return False

    def is_free(self):
        return self.value == "empty"

    def change(self, player):
        self.empty = 0
        if player == "circle":
            self.circle = 1
        else:
            self.square = 1


class TenBoard(Widget):
    index = NumericProperty(0)
    scale = NumericProperty(1)
    cube_size = NumericProperty(10)
    cube_padding = NumericProperty(10)
    circle = NumericProperty(0)
    square = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TenBoard, self).__init__(**kwargs)
        self.bind(pos=self.relayout, size=self.relayout)
        self.cells = []
        self.animations = []

        for index in range(9):
            cell = TenCell(index=index)
            self.add_widget(cell)
            self.cells.append(cell)
        self.relayout()

    def relayout(self, *args):
        xmin, ymin, cs, s, padding = self.cube_info
        x = xmin
        y = ymin

        for index, cell in enumerate(self.cells):
            cell.pos = x, y
            cell.size = cs, cs
            if index % 3 == 2:
                x = xmin
                y += cs + padding
            else:
                x += cs + padding

    @property
    def value(self):
        if self.circle == 1:
            return "circle"
        else:
            if self.square == 1:
                return "square"
            else:
                return "empty"

    @property
    def cube_info(self):
        s = 1

        padding = (s / 3.) / div_padding_cell
        cs = (s - (padding * 2)) / 3.
        xmin = 0
        ymin = 0
        return xmin, ymin, cs, s, padding

    def collide_point(self, x, y):
        x = (x - self.x) / self.scale
        y = (y - self.y) / self.scale
        x += self.x
        y += self.y
        return super(TenBoard, self).collide_point(x, y)

    def play_here(self, touch, player):
        for index, cell in enumerate(self.cells):
            if cell.collide_point(*touch.pos):
                if cell.is_free():
                    cell.change(player)
                    return cell.index
            continue
        return -1

    def is_free(self):
        return self.square == 0 and self.circle == 0

    def change(self):
        player = self.parent.players[self.parent.number_of_tour % 2]
        self.clear_widgets()
        self.cells = []
        if player == "circle":
            self.circle = 1
        else:
            self.square = 1
        self.parent.unfocus()

    def check(self):
        cells_value = [cell.value for cell in self.cells]
        for i in range(3):
            if cells_value[i] == cells_value[i+3] == cells_value[i+6] != "empty":
                self.change()
                return True
        for i in range(0, 7, 3):
            if cells_value[i] == cells_value[i+1] == cells_value[i+2] != "empty":
                self.change()
                return True
        if cells_value[0] == cells_value[4] == cells_value[8] != "empty":
            self.change()
            return True
        if cells_value[6] == cells_value[4] == cells_value[2] != "empty":
            self.change()
            return True

    def destroy(self):
        while self.cells:
            self.remove_widget(self.cells.pop())


class TenBoardLayout(Layout):
    circle = NumericProperty(0)
    square = NumericProperty(0)
    board_focused_index = NumericProperty(-1)
    players = ["circle", "square"]
    number_of_tour = 0

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
        index = self.board_focused_index
        board = self.board_focused
        if index == -1:
            for _index, _board in enumerate(self.boards):
                _board.pos = x, y
                _board.scale = cs
                if _index % 3 == 2:
                    x = xmin
                    y += cs + padding
                else:
                    x += cs + padding
        else:
            if index == 4:
                x, y, cs_board_focus, _xmin, _ymin, _cs, _padding = self.cube_info_focus_milieu
            else:
                x, y, cs_board_focus, _xmin, _ymin, _cs, _padding = self.cube_info_focus

            board.pos = x, y
            board.scale = cs_board_focus

            _x = _xmin
            _y = _ymin

            for _index, _board in enumerate(self.boards):
                if board is not _board:
                    _board.pos = _x, _y
                    _board.scale = _cs
                if _index % 3 == 2:
                    _x = _xmin
                    _y += _cs + _padding
                else:
                    _x += _cs + _padding

    @property
    def cube_info(self):
        s = min(self.width, self.height)

        padding = (s / 3.) / div_padding_board
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
        cs_board_focused = 2 * cs + padding

        slide_x = 0
        slide_y = 0
        if index == 0 or index == 3 or index == 6:
            slide_x = cs_board_focused + padding
        if index == 2 or index == 5 or index == 8:
            slide_x = - padding - cs
        if index == 1 or index == 7:
            slide_x = 0.5 * cs + 0.5 * padding
        if index == 0 or index == 1 or index == 2:
            slide_y = cs_board_focused + padding
        if index == 3 or index == 5:
            slide_y = 0.5 * cs + 0.5 * padding
        if index == 6 or index == 7 or index == 8:
            slide_y = - padding - cs

        _side = cs
        _padding = (_side / 3.) / div_padding_board
        _cs = (_side - (_padding * 4)) / 3.
        _xmin = x + slide_x + _padding
        _ymin = y + slide_y + _padding
        return x, y, cs_board_focused, _xmin, _ymin, _cs, _padding

    @property
    def cube_info_focus_milieu(self):

        xmin, ymin, cs, side, padding = self.cube_info
        t = math.ceil(((1 / 3.) / -2.) * 2.) / 2.
        x = xmin + ((1 % 3) + (1 % 3) / -2.) * (cs + padding)
        y = ymin + (int(1 / 3) + t) * (cs + padding)
        cs_board_focused = 2 * cs + padding

        _side = cs
        _padding = (_side / 3.) / div_padding_board
        _cs = (_side - (_padding * 4)) / 3.
        _xmin = x + 0.5 * cs + 0.5 * padding + _padding
        _ymin = y + cs_board_focused + padding + _padding
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
        self.animate(board, x=x, y=y, scale=cs_board_focus)

        _x = _xmin
        _y = _ymin

        for _index, _board in enumerate(self.boards):
            if board is not _board:
                self.animate(_board, x=_x, y=_y, scale=_cs)
            if _index % 3 == 2:
                _x = _xmin
                _y += _cs + _padding
            else:
                _x += _cs + _padding

    def unfocus(self):
        index = self.board_focused_index
        if index == -1:
            return
        xmin, ymin, cs, s, padding = self.cube_info
        x = xmin
        y = ymin
        self.stop_animations()
        for index, board in enumerate(self.boards):
            self.animate(board, x=x, y=y, scale=cs)
            if index % 3 == 2:
                x = xmin
                y += cs + padding
            else:
                x += cs + padding

        self.board_focused_index = -1

    def stop_animations(self):
        for anim, widget in self.animations:
            anim.stop_all(widget)
        self.animations = []

    def animate(self, widget, **kwargs):
        kwargs['d'] = .65
        kwargs['t'] = 'out_quart'
        anim = Animation(**kwargs)
        anim.start(widget)
        self.animations.append((anim, widget))
        return anim

    def change(self):
        player = self.players[self.number_of_tour % 2]
        self.clear_widgets()
        self.boards = []
        if player == "circle":
            self.circle = 1
        else:
            self.square = 1

    def check(self):
        for i in range(3):
            if self.boards[i].value == self.boards[i+3].value == self.boards[i+6].value != "empty":
                self.change()
                return True
        for i in range(0, 7, 3):
            if self.boards[i].value == self.boards[i+1].value == self.boards[i+2].value != "empty":
                self.change()
                return True
        if self.boards[0].value == self.boards[4].value == self.boards[8].value != "empty":
            self.change()
            return True
        if self.boards[6].value == self.boards[4].value == self.boards[2].value != "empty":
            self.change()
            return True

    def on_touch_down(self, touch):
        for index_board, board in enumerate(self.boards):
            if board.collide_point(*touch.pos) and board.is_free():
                if self.board_focused_index == index_board:
                    # si different de -1 le coup est prit en compte
                    index_cell = board.play_here(touch, self.players[self.number_of_tour % 2])
                    if index_cell != -1:
                        board.check()
                        if self.check():
                            self.end()
                            return
                        if self.boards[index_cell].is_free():
                            self.focus(index_cell)
                        self.number_of_tour += 1
                else:
                    self.unfocus()
                    self.focus(index_board)
                continue
        return True

    def end(self):
        end = self.ids.end.__self__
        self.remove_widget(end)
        self.add_widget(end)
        text = 'Player ' + self.players[self.number_of_tour % 2] + ' win !!'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)

    def restart(self):
        self.ids.end.opacity = 0
        self.number_of_tour = 0
        while self.boards:
            board = self.boards.pop()
            board.destroy()
            self.remove_widget(board)
        self.boards = []
        for index in range(9):
            board = TenBoard(index=index)
            self.add_widget(board)
            self.boards.append(board)
        self.relayout()


class TenApp(App):
    def build(self):
        return TenBoardLayout()

if __name__ == '__main__':
    TenApp().run()
