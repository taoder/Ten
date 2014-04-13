__version__ = '0.1.0'
import kivy
kivy.require('1.8.0')

from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.clock import Clock
from functools import partial
import math


div_padding_board = 5
div_padding_cell = 2


class RestartButton(ButtonBehavior, Label):
    layout = ObjectProperty()

    def on_press(self):
        print('lolo')
        self.layout.restart()


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

    def change(self, index_cell):
        player = self.parent.players[self.parent.number_of_tour % 2]
        cell = self.cells[index_cell]
        self.destroy()
        if player == "circle":
            self.circle = 1
        else:
            self.square = 1
        x = self.x
        y = self.y
        scale = self.scale

        self.pos = self.x + self.scale * cell.x, self.y + self.scale * cell.y
        self.scale = cell.size[0] * self.scale

        self.parent.animate(self, x=x, y=y, scale=scale)

    def check(self, index_cell):
        cells_value = [cell.value for cell in self.cells]
        for i in range(3):
            if cells_value[i] == cells_value[i+3] == cells_value[i+6] != "empty":
                self.change(index_cell)
                return True
        for i in range(0, 7, 3):
            if cells_value[i] == cells_value[i+1] == cells_value[i+2] != "empty":
                self.change(index_cell)
                return True
        if cells_value[0] == cells_value[4] == cells_value[8] != "empty":
            self.change(index_cell)
            return True
        if cells_value[6] == cells_value[4] == cells_value[2] != "empty":
            self.change(index_cell)
            return True

    def destroy(self):
        self.clear_widgets()
        self.cells = []


class TenBoardLayout(Layout):
    circle = NumericProperty(0)
    square = NumericProperty(0)
    cube_size = NumericProperty()
    cube_x = NumericProperty()
    cube_y = NumericProperty()
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
        if not self.is_free():
            xmin, ymin, cs, s, padding = self.cube_info
            self.cube_size = s - 2 * padding
            self.cube_x = xmin
            self.cube_y = ymin
            return
        index = self.board_focused_index
        board = self.board_focused
        if index == -1:
            xmin, ymin, cs, s, padding = self.cube_info
            x = xmin
            y = ymin

            self.cube_size = s - 2 * padding
            self.cube_x = xmin
            self.cube_y = ymin

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

    def destroy(self):
        for board in self.boards:
            board.destroy()
        self.clear_widgets()
        self.boards = []

    def is_free(self):
        return self.square == 0 and self.circle == 0

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
        board = self.board_focused
        anchor = self.ids.anchor.__self__
        self.remove_widget(anchor)
        self.add_widget(anchor)
        self.destroy()
        if player == "circle":
            self.circle = 1
        else:
            self.square = 1
        x = anchor.x
        y = anchor.y
        size = anchor.size

        anchor.pos = board.x, board.y
        anchor.size = board.size

        self.animate(anchor, x=x, y=y, size=size)

    def check(self, index_cell):
        t = 0.5
        if self.board_focused.check(index_cell):
            t = 1.5
            boards = [board.value for board in self.boards]
            for i in range(3):
                if boards[i] == boards[i+3] == boards[i+6] != "empty":
                    self.change()
                    return True
            for i in range(0, 7, 3):
                if boards[i] == boards[i+1] == boards[i+2] != "empty":
                    self.change()
                    return True
            if boards[0] == boards[4] == boards[8] != "empty":
                self.change()
                return True
            if boards[6] == boards[4] == boards[2] != "empty":
                self.change()
                return True
        Clock.schedule_once(partial(self.next_player, index_cell), t)

    def on_touch_down(self, touch):
        if not self.is_free():
            super(TenBoardLayout, self).on_touch_down(touch)
        else:
            for index_board, board in enumerate(self.boards):
                if board.collide_point(*touch.pos) and board.is_free():
                    if self.board_focused_index == -1:
                        self.focus(index_board)
                        return
                    if self.board_focused_index == index_board:
                        # si different de -1 le coup est prit en compte
                        index_cell = board.play_here(touch, self.players[self.number_of_tour % 2])
                        if index_cell != -1:
                            if self.check(index_cell):
                                Clock.schedule_once(self.end, 0.5)
                                return True
                    return True

    def next_player(self, index_cell, *largs):
        if self.boards[index_cell].is_free():
            self.focus(index_cell)
        else:
            self.unfocus()
        self.number_of_tour += 1

    def end(self, *largs):
        end = self.ids.end.__self__
        #self.remove_widget(end)
        #self.add_widget(end)
        text = 'Player ' + self.players[self.number_of_tour % 2] + ' win !!'
        self.ids.end_label.text = text
        Animation(opacity=1., d=.5).start(end)

    def restart(self):
        self.ids.end.opacity = 0
        self.number_of_tour = 0
        self.board_focused_index = -1
        self.circle = 0
        self.square = 0

        for board in self.boards:
            board.destroy()
        self.clear_widgets()
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
    Factory.register('RestartButton', cls=RestartButton)
    TenApp().run()
