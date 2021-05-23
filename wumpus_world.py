#made By R3dzone
import random

global direction

direction = [[0,1], #direcion[0] East
             [1,0], #direcion[1] North
             [0,-1], #direcion[2] West
             [-1,0]] #direcion[3] South

class Agent:
    def __init__(self):
        print("new Agent")

class World:
    def __init__(self):
        world_state = [[[0],[0],[0],[0]], #world_state[y][x]
                       [[0],[0],[0],[0]],
                       [[0],[0],[0],[0]],
                       [[0],[0],[0],[0]]]
        #0 = not signal
        #1 = gold
        #2 = wumpus
        #3 = pit
        #4 = gliter
        #5 = stench
        #6 = breeze
        #7 = bump
        #8 = scream

        """
        환경생성
        """
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
            world_state = [[[0], [0], [0], [0]], #world_state[y][x]
                           [[0], [0], [2], [0]],
                           [[0], [3], [1], [0]],
                           [[0], [0], [0], [0]]]

        """
        신호주기
        """
        for i in range(0, 16):
            #print(str(int(i / 4)) + "," + str(int(i % 4)) + ":" + str(world_state[int(i / 4)][int(i % 4)]))
            #print("x:"+str(int(i % 4))+"y:"+str(int(i / 4)) + ":"+str(world_state[int(i / 4)][int(i % 4)]))
            y = int(i / 4)
            x = int(i % 4)
            if(world_state[y][x][0] > 0 and world_state[y][x][0] < 4): #Wumpus or Gold or Pit
                tmp_state = world_state[int(i / 4)][int(i % 4)][0] + 3
                for j in range(0,4):
                    y = int(i / 4) + direction[j][0]
                    x = int(i % 4) + direction[j][1]
                    if( x >= 0 and x < 4 and y >= 0 and y < 4):
                        #print(str(x)+","+str(y))
                        world_state[y][x].append(tmp_state)

        print(world_state)

    def make(self):
        print("run")

if __name__ == "__main__":
    Wumpus_World = World()