import random
import time
from tkinter import Tk, Canvas, Label
from threading import Timer

root = Tk()


class Game:
    SQUARE_SIZE = 25

    def __init__(self, root, width, height):
        self.width = width
        self.height = height
        self.MAX_HEIGHT = height / self.SQUARE_SIZE
        self.MAX_WIDTH = width / self.SQUARE_SIZE
        print('self.MAX_HEIGHT =', self.MAX_HEIGHT)
        self._canvas = Canvas(root, width=width, height=height, background='black')
        self._canvas.pack()
        self._snake = Snake(self)
        self._apples = []
        self._score = 0
        self._lblScore = Label(root, text='Score: 0')
        self._lblScore.pack()

        self._sprites = {
            # obj: canvasID,
            self._snake: self._canvas.create_rectangle(0, 0, 0, 0, fill='lightgreen')
        }

        root.bind("<Key>", self.HandleKeyEvent)

        self.gameOver = False
        self.delay = 0.1

    def HandleKeyEvent(self, event):
        print('HandleKeyEvent(', event)
        opposite = {
            'left': 'right',
            'up': 'down',
            'down': 'up',
            'right': 'left'
        }
        if self._snake.direction != opposite.get(event.keysym.lower()):
            self._snake.direction = event.keysym.lower()

    def Update(self):
        # print('Update')
        self._snake.Move()

        if self._snake.position in self._snake.pieces[1:]:
            self.GameOver()

        if self.MAX_WIDTH >= self._snake.position[0] < 0:
            self.GameOver()
        elif self.MAX_HEIGHT >= self._snake.position[1] < 0:
            self.GameOver()

        for index, piece in enumerate(self._snake.pieces):
            ID = self._sprites.get(index, None)
            if ID is None:
                ID = self._sprites[index] = self._canvas.create_rectangle(
                    (
                        piece[0] * self.SQUARE_SIZE,
                        piece[1] * self.SQUARE_SIZE,
                        piece[0] * self.SQUARE_SIZE + self.SQUARE_SIZE,
                        piece[1] * self.SQUARE_SIZE + self.SQUARE_SIZE
                    ),
                    fill='lightgreen' if index is 0 else 'green'
                )

            self._canvas.coords(
                ID,
                (
                    piece[0] * self.SQUARE_SIZE,
                    piece[1] * self.SQUARE_SIZE,
                    piece[0] * self.SQUARE_SIZE + self.SQUARE_SIZE,
                    piece[1] * self.SQUARE_SIZE + self.SQUARE_SIZE
                )
            )

        if len(self._apples) is 0:
            self.NewApple()

        for apple in self._apples:
            ID = self._sprites.get(apple, None)
            if ID is None:
                ID = self._sprites[apple] = self._canvas.create_oval(
                    apple.x,
                    apple.y,
                    apple.x + Game.SQUARE_SIZE,
                    apple.y + Game.SQUARE_SIZE,
                    fill='red',
                )

            if self._snake.position == apple.position:
                self._score += 1
                self._lblScore.config(text=f'Score: {self._score}')
                self._canvas.delete(ID)
                self._apples.remove(apple)
                self._snake.AddTail()

                self.delay *= 0.98 # speed up each time you eat an apple

            else:

                self._canvas.coords(
                    ID,
                    (
                        apple.position[0] * self.SQUARE_SIZE,
                        apple.position[1] * self.SQUARE_SIZE,
                        apple.position[0] * self.SQUARE_SIZE + self.SQUARE_SIZE,
                        apple.position[1] * self.SQUARE_SIZE + self.SQUARE_SIZE
                    )
                )

    def GameOver(self):
        print('GAME OVER')
        self.gameOver = True

    def NewApple(self):
        self._apples.append(Apple(self))


class Snake:
    def __init__(self, host):
        self._host = host
        self._length = 1
        self.pieces = [
            [
                int((host.width / Game.SQUARE_SIZE) / 2),
                int((host.height / Game.SQUARE_SIZE) / 2)
            ]
        ]
        self.direction = 'up'
        self._addTailOnNextMove = False

    def AddTail(self):
        self._addTailOnNextMove = True

    def Move(self):

        newHead = self.pieces[0].copy()

        if self.direction == 'up':
            newHead[1] = self.pieces[0][1] - 1
        elif self.direction == 'down':
            newHead[1] = self.pieces[0][1] + 1
        elif self.direction == 'left':
            newHead[0] = self.pieces[0][0] - 1
        elif self.direction == 'right':
            newHead[0] = self.pieces[0][0] + 1

        self.pieces.insert(0, newHead)
        # print('self.pieces=', self.pieces)
        if self._addTailOnNextMove is True:
            self._addTailOnNextMove = False
        else:
            self.pieces.pop()  # remove the right most piece

    @property
    def position(self):
        return self.pieces[0]


class Apple:
    def __init__(self, host, x=None, y=None):
        self.x = x or random.randint(0, host.MAX_WIDTH-1)
        self.y = y or random.randint(0, host.MAX_HEIGHT-1)
        self.position = [self.x, self.y]
        print('Apple.position=', self.position)


SIZE = 800
game = Game(root, SIZE, SIZE)


def Loop():
    while game.gameOver is False:
        game.Update()
        time.sleep(game.delay)


Timer(0, Loop).start()
root.mainloop()
