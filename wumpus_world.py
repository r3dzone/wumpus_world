#made By R3dzone
import random

class Agent:
    def __init__(self):
        print("new Agent")

class World:
    def __init__(self):
        world_state = [[[0],[0],[0],[0]],
                       [[0],[0],[0],[0]],
                       [[0],[0],[0],[0]],
                       [[0],[0],[0],[0]]]
        #0 = not signal
        #1 = gold
        #2 = wumpus
        #3 = pit
        #4 = stench
        #5 = breeze
        #6 = gliter
        #7 = bump
        #8 = scream

        if(input("random? y/n\n") == "y"):
            world_state[0][0][0] = 0 #safe
            for i in range(1,16):
                #world_state[int(i/4)][int(i%4)].append(1)
                if((int(i/4) == 0 and int(i%4) == 1) or (int(i/4) == 1 and int(i%4) == 0)):
                    continue
                print(str(int(i / 4)) + "," + str(int(i % 4)))
                if(random.choices(range(0,2),weights=[85,15]) == [1]):#15% 확률
                    world_state[int(i / 4)][int(i % 4)][0] = 3
                elif(random.choices(range(0,2),weights=[85,15]) == [1]):#15% 확률
                    world_state[int(i / 4)][int(i % 4)][0] = 2
                else:
                    world_state[int(i / 4)][int(i % 4)][0] = 0
        else:
            world_state = [[[0], [0], [0], [0]],
                           [[0], [0], [2], [0]],
                           [[0], [3], [1], [0]],
                           [[0], [0], [0], [0]]]
        print(world_state)

    def make(self):
        print("run")

if __name__ == "__main__":
    Wumpus_World = World()