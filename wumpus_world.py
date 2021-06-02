#made By R3dzone
import random
import os
import copy
import time

global direction

direction = [[0,1], #direcion[0] East
             [1,0], #direcion[1] North
             [0,-1], #direcion[2] West
             [-1,0]] #direcion[3] South

global state_key
state_key = {0 :"N",1 :"G",2 :"W",3 :"P",4 :"g",5 :"s",6 :"b",7 :"B",8 :"S"}

# 0 = not signal

# 1 = gold
# 2 = wumpus
# 3 = pit

# 4 = gliter
# 5 = stench
# 6 = breeze

# 7 = bump
# 8 = scream

global num_to_dir
num_to_dir = {0 :"E",1 :"N",2 :"W",3 :"S"}

global num_to_arrow
num_to_arrow = {0 :"→",1 :"↑",2 :"←",3 :"↓"}

global percept_key
percept_key = {0 :"U",1 :"G",2 :"W",3 :"P",4 :"S",5 :"G?",6 :"W?",7 :"P?",8:"V",9:"A"}

# 0 = Unknown

# 1 = gold
# 2 = wumpus
# 3 = pit
# 4 = Safe

# 5 = gold?
# 6 = wumpus?
# 7 = pit?

# 8 = Visited
# 9 = Agent

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
        self.position = [0,0] #x,y
        self.arrow_num = 3
        self.gold = False
        self.move_cnt = 0
        self.world = world #불변
        self.d_world = copy.deepcopy(self.world) #dynamic world
        self.world_percept = [[[4], [0], [0], [0]],  # world_state[y][x]
                             [[0], [0], [0], [0]],
                             [[0], [0], [0], [0]],
                             [[0], [0], [0], [0]]]
        self.move_stack = []

    def add_percept(self,y,x,state,dir_num):
        for j in range(0, 4):
            if(j == ((dir_num+2)%4)):
                continue
            tmp_y = y + direction[j][1]
            tmp_x = x + direction[j][0]
            if (tmp_x >= 0 and tmp_x < 4 and tmp_y >= 0 and tmp_y < 4):
                tmp = self.world_percept[tmp_y][tmp_x][0]
                if (tmp != 8 and tmp != 1 and tmp != 2 and tmp != 3 ):
                    if (tmp != 0):
                        self.world_percept[tmp_y][tmp_x].append(state)
                    else:
                        self.world_percept[tmp_y][tmp_x][0] = state

    def del_percept(self):
        print("del!")

    def get_action(self,action):
        self.print_world()

    def position_update(self,y,x):
        self.position[0] = y
        self.position[1] = x
        self.move_cnt += 1
        
        flag = True
        for i in range(len(self.world_percept[y][x])):
            if(self.world_percept[y][x][i] == 8):
                flag = False
            if (self.world_percept[y][x][i] == 0):
                del self.world_percept[y][x][i]

        if(flag): #방문한적이 없을 시
            die_flag = False
            percept_len = len(self.world_percept[y][x])
            for i in range(len(self.d_world[y][x])):
                if (self.d_world[y][x][i] == 2):  # wumpus가 있을 시 사망/Wumpus 위치 기록
                    die_flag = True
                    self.world_percept[y][x].append(2)
                    # 이전 stench 시그널들 삭제

                if (self.d_world[y][x][i] == 3):  # pit가 있을 시 사망 /pit 위치 기록
                    die_flag = True
                    self.world_percept[y][x].append(3)
                    # 이전 breeze시그널들 삭제

                if (self.d_world[y][x][i] == 1):  # Gold 위치 기록
                    self.world_percept[y][x].append(1)
                    # 이전 gliter시그널들 삭제
                if (self.d_world[y][x][i] == 4):  # gliter
                    self.add_percept(y, x, 5, self.A_direction)  # gold? state
                if (self.d_world[y][x][i] == 5):  # stench
                    self.add_percept(y, x, 6, self.A_direction)  # wumpus? state
                if (self.d_world[y][x][i] == 6):  # breeze
                    self.add_percept(y, x, 7, self.A_direction)  # pit? state

            del self.world_percept[y][x][0:percept_len]
            self.world_percept[y][x].append(8)
            if(die_flag):
                self.die()
            else:
                self.world_percept[y][x].append(4)


    def GoForward(self):
        y = direction[self.A_direction][1] + self.position[0]
        x = direction[self.A_direction][0] + self.position[1]
        if(y < 0 or y > 3 or x < 0 or x > 3):
            self.bump()
        else:
            self.position_update(y,x)
            self.move_stack.append("g")

    def TurnLeft(self):
        if(self.A_direction == 3):
            self.A_direction = 0
        else:
            self.A_direction += 1
        self.move_stack.append("l")

    def TurnRight(self):
        if(self.A_direction == 0):
            self.A_direction = 3
        else:
            self.A_direction -= 1
        self.move_stack.append("r")

    def bump(self):
        print("앞은 벽입니다! 다시 선택해주세요")

    def scream(self,y,x):
        for i in range(len(self.d_world[y][x])):
            if(self.d_world[y][x][i] == 2): #wumpus가 있었을 경우
                return True
            else:
                return False

    def Grab(self):
        if(self.d_world[self.position[0]][self.position[1]][0] == 1):   #Gold가 있을 시 Grab /Gold 위치 기록
            self.gold = True
            del self.d_world[self.position[0]][self.position[1]][0]
        else:
            print("골드가 없습니다!")

    def Shoot(self):
        if(self.arrow_num > 0):
            self.arrow_num -= 1
            y = direction[self.A_direction][1] + self.position[0]
            x = direction[self.A_direction][0] + self.position[1]
            if(self.scream(y,x)):
                print("wumpus를 제거했습니다!")
                print(self.d_world[y][x])
                print(self.world_percept[y][x])
                self.d_world[y][x] = [0]
                self.world_percept[y][x] = [2]
                #wumpus 시그널 삭제
            else:
                print("wumpus가 없었습니다!")
                #y,x에움퍼스없는거확인()

    def Climb(self):
        if(self.position[0] == 0 and self.position[1] == 0 and self.gold):
            print("clear")
        else:
            print("clear 조건을 만족하지 못했습니다.")

    def die(self):
        self.A_direction = 0 #intial direction - East
        self.position = [0,0] #y,x
        self.arrow_num = 3
        self.gold = False
        self.move_cnt = 0
        self.d_world = copy.deepcopy(self.world) #dynamic world
        self.move_stack = []

    def print_world(self):
        env = self.world_percept
        print("Agent's position is " +str(self.position[0]+1)+"," +str(self.position[1]+1))
        print("        direction is "+num_to_dir[self.A_direction])
        print("        arrow_num is " + str(self.arrow_num))
        if(self.gold):
            print("Agent have Gold!")

        for i in reversed(range(4)):
            print("╋━━━━━━" * 4 + "╋")
            line = ""
            agent_percept = ""
            for j in range(0, 4):
                env_len = len(env[j][i])
                len_tmp = env_len
                for k in range(env_len):
                    if(env[j][i][k] >= 5 and env[j][i][k] <= 7):
                        len_tmp += 1
                line += "┃" + " " * (6 - len_tmp)
                agent_percept += "┃" + " " * 4
                for k in range(env_len):
                    line += percept_key[env[j][i][k]]
                if (j == self.position[0] and i == self.position[1]):  # Agent가 위치한 자리에서
                    agent_percept += "A" + num_to_arrow[self.A_direction]
                else:
                    agent_percept += "  "
            print(line + "┃")
            print(agent_percept + "┃")
        print("╋━━━━━━" * 4 + "╋")

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

def human_control(real,agent):
    function_dict = {"g": agent.GoForward, "l": agent.TurnLeft, "r": agent.TurnRight, "s": agent.Shoot, "c": agent.Grab ,"cl": agent.Climb}

    while(True):
        os.system("cls")
        print("real environment!")
        print_world(real.world_state)
        print("agent's percept")
        agent.print_world()
        weight = [0, 0, 0, 0]
        for i in range(0, 4):
            tmp_y = agent.position[1] + direction[i][0]
            tmp_x = agent.position[0] + direction[i][1]
            # print(str(tmp_x+1)+","+str(tmp_y+1)+"확인")
            if (tmp_x >= 0 and tmp_x < 4 and tmp_y >= 0 and tmp_y < 4):
                for j in range(len(agent.world_percept[tmp_x][tmp_y])):
                    weight_dic = {0: 0, 1: 1000, 2: -1000, 3: -1000, 4: 0, 5: 1, 6: -1, 7: -1, 8: -100}
                    weight[i] += weight_dic[agent.world_percept[tmp_x][tmp_y][j]]
            else:
                weight[i] = -1000
            print(num_to_arrow[i] + str(tmp_x + 1) + "," + str(tmp_y + 1) + ":" + str(weight[i]))

        max_dir = agent.A_direction
        for i in range(0, 4):
            if (weight[(agent.A_direction + 1 + i) % 4] >= weight[max_dir]):
                max_dir = (agent.A_direction + 1 + i) % 4
        print("go " + num_to_arrow[max_dir])
        behavior = function_dict[input("어떻게 행동할까요?")]
        behavior()

def AI_control(real,agent):
    function_dict = {"g": agent.GoForward, "r": agent.TurnLeft, "l": agent.TurnRight, "s": agent.Shoot, "c": agent.Grab, "cl": agent.Climb}

    while(not agent.gold):
        os.system("cls")
        print("real environment!")
        print_world(real.world_state)
        print("agent's percept")
        agent.print_world()
        time.sleep(2)
        weight = [0, 0, 0, 0]
        for i in range(0, 4):
            tmp_y = agent.position[1] + direction[i][0]
            tmp_x = agent.position[0] + direction[i][1]
            # print(str(tmp_x+1)+","+str(tmp_y+1)+"확인")
            if (tmp_x >= 0 and tmp_x < 4 and tmp_y >= 0 and tmp_y < 4):
                for j in range(len(agent.world_percept[tmp_x][tmp_y])):
                    weight_dic = {0: 0, 1: 1000, 2: -1000, 3: -1000, 4: 0, 5: 1, 6: -1, 7: -1, 8: -100}
                    weight[i] += weight_dic[agent.world_percept[tmp_x][tmp_y][j]]
            else:
                weight[i] = -1000
            print(num_to_arrow[i] + str(tmp_x + 1) + "," + str(tmp_y + 1) + ":" + str(weight[i]))

        max_dir = agent.A_direction
        for i in range(0, 4):
            if (weight[(agent.A_direction + 1 + i) % 4] >= weight[max_dir]):
                max_dir = (agent.A_direction + 1 + i) % 4
        print("go " + num_to_arrow[max_dir])
        while(max_dir != agent.A_direction):
            agent.TurnLeft()
            os.system("cls")
            print("real environment!")
            print_world(real.world_state)
            print("agent's percept")
            agent.print_world()
            time.sleep(1)
        agent.GoForward()
        print(agent.move_stack)
        if(agent.d_world[agent.position[0]][agent.position[1]][0] == 1):
            agent.Grab()
            agent.TurnLeft()
            agent.TurnLeft()
            for i in reversed(range(len(agent.move_stack)-2)):
                print("실행")
                print(i)
                function_dict[agent.move_stack[i]]()
                os.system("cls")
                print("real environment!")
                print_world(real.world_state)
                print("agent's percept")
                agent.print_world()
                time.sleep(1)
            agent.Climb()

if __name__ == "__main__":
    Wumpus_World = World()
    user_Agent = Agent(Wumpus_World.world_state)
    control = input("select control mode! [h: human control/a or another: AI control]")
    if(control == "h"):
        human_control(Wumpus_World,user_Agent)
    else:
        AI_control(Wumpus_World,user_Agent)
