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

def key_hook(delay: float, agent: DQNAgent) -> float:
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

def game(iteration: int, viz: bool, win):
    delay = 0
    agent = DQNAgent(12, 4)
    try:
        for i in range(iteration):
            board = init_board()
            if viz:
                render(board, win)
                py.display.update()
            steps = 0
            total_reward = 0
            while 1:
                delay = key_hook(delay, agent)
                time.sleep(delay)
                reward, running = ai_decision(board, agent, win, viz)
                total_reward += reward
                if not running:
                    if i > iteration - iteration:
                        print(f"Episode #{i} is over with a total score of {total_reward:.1f} and length {find_length(board)} after {steps} steps")
                    break
                steps += 1
    except KeyboardInterrupt or exitTrainingProgram as e:
        print(e)
        py.quit()
        exit(0)
    
    jb.dump(agent, "model.ml")

def main():
    global close
    close = False
    viz = False
    iteration = 0
    win = None

    try:
        i = sys.argv.index('-i') + 1
        iteration = int(sys.argv[i])
        if iteration <= 0:
            print(f"Please enter the amount of iterations greater than 0")
    except:
        print(f"Please enter the amount of iterations with the flag -i num_of_iterations")
        exit(1)

    py.init()
    if '-v' in sys.argv:
        viz = True
        win = py.display.set_mode((macro.WIDTH, macro.HEIGHT))
        py.display.set_caption("Snake Game") 

    game(iteration, viz, win)
    py.quit()
    exit(0)

if __name__ == '__main__':
    main()