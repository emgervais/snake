import pygame as py
import macro
from init import init_board
from utils import find_length
from ai import ai_decision
from render import render
from DQN import DQNAgent
import joblib as jb
import sys
import time


class exitTrainingProgram(Exception):
    pass


class snakeGame:
    def __init__(self, agent, viz, iteration, evaluate, size):
        self.agent = agent
        self.viz = viz
        self.iteration = iteration
        self.win = None
        self.delay = 0
        self.size = size + 2
        self.step = False
        self.square_size = macro.HEIGHT / self.size
        if self.viz:
            py.init()
            self.win = py.display.set_mode((macro.WIDTH, macro.HEIGHT))
            py.display.set_caption("Snake Game")

        if evaluate:
            self.agent.epsilon = -1
            self.delay = 1

        if "-step" in sys.argv:
            self.step = True


def key_hook(delay: float, agent: DQNAgent, step: bool) -> float:
    if step:
        while 1:
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT:
                        return 0
                    elif event.key == py.K_s:
                        jb.dump(agent, "model")
                    elif event.key == py.K_ESCAPE:
                        raise exitTrainingProgram
            time.sleep(0.1)
    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT and delay - 0.05 >= 0:
                delay -= 0.05
            elif event.key == py.K_RIGHT:
                delay += 0.05
            elif event.key == py.K_s:
                jb.dump(agent, "model")
            elif event.key == py.K_ESCAPE:
                raise exitTrainingProgram
    return delay


def game(snakeGame: snakeGame):
    try:
        for i in range(snakeGame.iteration):
            food_eaten = 0
            counter = 0
            board = init_board(snakeGame.size, snakeGame.square_size)
            if snakeGame.viz:
                render(board, snakeGame.square_size, snakeGame.win)
                py.display.update()
            total_reward = 0
            while 1:
                if snakeGame.viz:
                    snakeGame.delay = key_hook(snakeGame.delay,
                                               snakeGame.agent, snakeGame.step)
                    time.sleep(snakeGame.delay)
                reward, running, food_eaten, counter =\
                    ai_decision(board, snakeGame, food_eaten, counter)
                total_reward += reward
                if not running:
                    print(f"Episode #{i} is over \
                          with a total score of \
                          {total_reward:.1f} and length {find_length(board)}")
                    break
            if i % 10000 == 0:
                jb.dump(snakeGame.agent, f"snake_dqn_{i + 80000}.h5")
    except KeyboardInterrupt or exitTrainingProgram as e:
        print(e)
        py.quit()
        jb.dump(snakeGame.agent, "model.ml")
        exit(0)

    jb.dump(snakeGame.agent, "model.ml")
    py.quit()


def init_params():
    agent = DQNAgent(8, 4)
    try:
        i = sys.argv.index('-i') + 1
        iteration = int(sys.argv[i])
        if iteration <= 0:
            print("Please enter the amount of iterations greater than 0")
    except ValueError or IndexError:
        print("Please enter the amount of iterations \
              with the flag -i num_of_iterations")
        exit(1)
    viz = True if "-v" in sys.argv else False
    evaluate = True if "-e" in sys.argv else False
    agent = DQNAgent(8, 4)
    size = 10
    if "-board" in sys.argv:
        try:
            index = sys.argv.index("-board") + 1
            size = int(sys.argv[index])
            if size <= 0:
                print("Please enter a size greater than 0")
                exit(1)
        except ValueError or IndexError:
            print("Please enter a size after the flag -board")
            exit(1)
    if "-l" in sys.argv or evaluate:
        try:
            if evaluate:
                index = sys.argv.index("-e") + 1
            else:
                index = sys.argv.index("-l") + 1
            agent = jb.load(sys.argv[index])
        except ValueError or IndexError:
            print("Please enter the model file to load")
            exit(1)
    snake = snakeGame(agent, viz, iteration, evaluate, size)
    return snake


def main():
    snakeGame = init_params()
    game(snakeGame)


if __name__ == '__main__':
    main()
