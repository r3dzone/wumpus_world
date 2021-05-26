#made By R3dzone
import random

global direction

direction = [[0,1], #direcion[0] East
             [1,0], #direcion[1] North
             [0,-1], #direcion[2] West
             [-1,0]] #direcion[3] South

global state_key
state_key = {0 :"N",1 :"G",2 :"W",3 :"P",4 :"g",5 :"s",6 :"b",7 :"B",8 :"S"}

global num_to_dir
num_to_dir = {0 :"E",1 :"N",2 :"W",3 :"S"}

global percept_key
percept_key = {0 :"U",1 :"G",2 :"W",3 :"P",4 :"g",5 :"s",6 :"b",9:"A"}

# 0 = not signal

# 1 = gold
# 2 = wumpus
# 3 = pit

# 4 = gliter
# 5 = stench
# 6 = breeze

# 7 = bump
# 8 = scream

def print_world(env):
    for i in reversed(range(4)):
        print("╋━━━"*4+"╋")
        line = ""
        for j in range(0, 4):
            env_len = len(env[j][i])
            line += "┃" + " "*(3-env_len)
            for k in range(0,env_len):
                line += state_key[env[j][i][k]]
        print(line + "┃")
    print("╋━━━" * 4 + "╋")

class Agent:
    def __init__(self,world):
        print("new Agent")
        self.A_direction = 0 #intial direction - East
        self.position = [0,0] #y,x
        self.arrow_num = 3
        self.gold = False
        self.world = world
        self.world_percept = [[[0], [0], [0], [0]],  # world_state[y][x]
                             [[0], [0], [0], [0]],
                             [[0], [0], [0], [0]],
                             [[0], [0], [0], [0]]]

    def position_update(self,y,x):
        self.position[0] = y
        self.position[1] = x

    def GoForward(self):
        y = direction[self.A_direction] + self.position[0]
        x = direction[self.A_direction] + self.position[1]
        if(y < 0 or y > 3 or x < 0 or x > 3):
            self.bump()
        else:
            self.position_update(y,x)

    def TurnLeft(self):
        if(self.A_direction == 3):
            self.A_direction = 0
        else:
            self.A_direction += 1

    def TurnRight(self):
        if(self.A_direction == 0):
            self.A_direction = 3
        else:
            self.A_direction -= 1

    #def bump(self):

    #def scream(self,y,x):

    def Grab(self):
        self.gold = True

    def Shoot(self):
        if(self.arrow_num > 0):
            self.arrow_num -= 1
            y = direction[self.A_direction] + self.position[0]
            x = direction[self.A_direction] + self.position[1]
            """
            if(self.scream(y,x)):
                wumpus제거()
            else:
                y,x에움퍼스없는거확인()
            """

    #def Climb(self):

    def print_world(self):
        env = self.world_percept
        print("Agent's position is " +str(self.position[1]+1)+"," +str(self.position[0]+1))
        print("        direction is "+num_to_dir[self.A_direction])
        print("        arrow_num is " + str(self.arrow_num))
        if(self.gold):
            print("Agent have Gold!")

        for i in reversed(range(4)):
            print("╋━━━" * 4 + "╋")
            line = ""
            for j in range(0, 4):
                env_len = len(env[j][i])
                line += "┃" + " " * (3 - env_len)
                if( i == self.position[0] and j == self.position[1]): #Agent가 위치한 자리에서
                    line = line[:-1]
                    line += "A"
                for k in range(0, env_len):
                    line += percept_key[env[j][i][k]]
            print(line + "┃")
        print("╋━━━" * 4 + "╋")



class World:
    def __init__(self):
        self.world_state = [[[0], [0], [0], [0]],  # world_state[y][x]
                       [[0], [0], [0], [0]],
                       [[0], [0], [0], [0]],
                       [[0], [0], [0], [0]]]

        """
        환경생성
        """
        if(input("random? y/n\n") == "y"):
            self.world_state[0][0][0] = 0 #safe
            for i in range(1,16):
                #world_state[int(i/4)][int(i%4)].append(1)
                if((int(i/4) == 0 and int(i%4) == 1) or (int(i/4) == 1 and int(i%4) == 0)):
                    continue
                print(str(int(i / 4)) + "," + str(int(i % 4)))
                if(random.choices(range(0,2),weights=[85,15]) == [1]):#15% 확률
                    self.world_state[int(i / 4)][int(i % 4)][0] = 3
                elif(random.choices(range(0,2),weights=[85,15]) == [1]):#15% 확률
                    self.world_state[int(i / 4)][int(i % 4)][0] = 2
                else:
                    self.world_state[int(i / 4)][int(i % 4)][0] = 0
        else:
            self.world_state = [[[0], [0], [0], [0]], #world_state[y][x] 90도 시계 rotation
                                [[0], [0], [1], [0]],
                                [[0], [2], [3], [0]],
                                [[0], [0], [0], [0]]]

        """
        신호주기
        """
        for i in range(0, 16):
            #print(str(int(i / 4)) + "," + str(int(i % 4)) + ":" + str(world_state[int(i / 4)][int(i % 4)]))
            #print("x:"+str(int(i % 4))+"y:"+str(int(i / 4)) + ":"+str(world_state[int(i / 4)][int(i % 4)]))
            y = int(i / 4)
            x = int(i % 4)
            if(self.world_state[y][x][0] > 0 and self.world_state[y][x][0] < 4): #Wumpus or Gold or Pit
                tmp_state = self.world_state[int(i / 4)][int(i % 4)][0] + 3
                for j in range(0,4):
                    y = int(i / 4) + direction[j][0]
                    x = int(i % 4) + direction[j][1]
                    if( x >= 0 and x < 4 and y >= 0 and y < 4):
                        #print(str(x)+","+str(y))
                        if(self.world_state[y][x][0] != 0):
                            self.world_state[y][x].append(tmp_state)
                        else:
                            self.world_state[y][x][0] = tmp_state

if __name__ == "__main__":
    Wumpus_World = World()
    user_Agent = Agent(Wumpus_World.world_state)
    print("real environment!")
    print_world(Wumpus_World.world_state)
    print("agent's percept")
    user_Agent.print_world()