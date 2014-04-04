from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_string('''
#:import random random.random
<TenBoard>:
    canvas:
        Color:
            hsv: random(), .2, .4
            a: .2
        Rectangle:
            pos: self.pos
            size: self.size
''')

class TenBoard(Widget):
    index = NumericProperty(0)
    
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.parent.board_focused_index == self.index:
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
        self.anim = None
        self.boards = []
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
        if self.anim:
            self.anim.stop_all(board)
        xmin, ymin, cs, side = self.cube_info
        print(index)
        t = (index / 3.) / -2.
        print(t)
        print(((index % 3) + t))
        print((int(index / 3) + t))

        x = xmin + ((index % 3) + (index % 3) / -2.) * cs
        y = ymin + (int(index / 3) + t) * cs
        self.anim = Animation(pos=(x, y), size=(side/1.5, side/1.5))
        self.anim.start(board)
        
    def unfocus(self):
        index = self.board_focused_index
        if index == -1:
            return
        xmin, ymin, cs, side = self.cube_info
        x = xmin + (index % 3) * cs
        y = ymin + int(index / 3) * cs
        if self.anim:
            self.anim.stop_all(self.board_focused)
        self.anim = Animation(pos=(x, y), size=(cs, cs))
        self.anim.start(self.board_focused)
        self.board_focused_index = -1
        
if __name__ == '__main__':
    class TenBoardApp(App):
        def build(self):
            return TenBoardLayout()
    TenBoardApp().run()