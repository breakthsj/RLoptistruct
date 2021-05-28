import time
import numpy as np
import csv
import math
import fusion360_com
from pywinauto.application import Application
import pywinauto
import pandas as pd

np.random.seed(1)


class Env:
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r', 'f', 'b']
        self.action_size = len(self.action_space)

        self.counter = 0

        # 실행중 프로세스 받아오기
        procs = pywinauto.findwindows.find_elements()

        # 실행 중 프로세스에서 fusion360 찾기
        for proc in procs:
            if proc.name == 'Autodesk Fusion 360 (Personal - Not for Commercial Use)':
                print("찾았다!")
                break

        # 프로세스로 fusion360 연결
        app = Application(backend="uia").connect(process=proc.process_id)

        # dialog 연결
        self.dig = app['{}'.format(proc.name)]


    def set_reward(self, state):
        state = [int(state[0]), int(state[1]), int(state[2]), int(state[3])]
        x = int(state[0])
        y = int(state[1])
        z = int(state[2])
        C = int(state[3])

        # 원점으로부터 생성위치 거리
        loc_dist = math.sqrt(x*x+y*y+z*z)

        # 리워드 생성 (무게중심과 원점이 멀수록 -, 생성위치거리가 2보다 작으면 -)
        reward = -C
        if (loc_dist-2) < 0:
            reward -= 0.3

        return reward

    def reset(self):
        time.sleep(0.5)
        self.counter = 0
        #reset position
        s_ = [{'X': 0, 'Y': 0, 'Z': 0, 'C': 0}]

        # csv 파일 작성하기_새로운 액션에 대한
        csv_dir = r"C:\Users\break\Downloads\RLop\RLoptistruct\Demo\demo_com_0514\demo_com.csv"
        field = ['X', 'Y', 'Z', 'C']
        with open(csv_dir, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writeheader()
            writer.writerows(s_)

        return self.get_state()

    def step(self, action):
        self.counter += 1

        # state를 받아옴
        state = self.get_state()

        # 액션에 따라 움직임
        self.move(state, action)

        # 완료여부, 리워드 설정
        if self.counter > 49:
            done = True
        else:
            done = False
        reward = self.set_reward(state)

        s_ = self.get_state()

        return s_, reward, done

    def move(self, state, action):
        # 액션에 따라 생성좌표 변화
        if action == 0:  # +x
            state[0] += 1
        elif action == 1:  # -x
            state[0] -= 1
        elif action == 2:  # +y
            state[1] += 1
        elif action == 3:  # -y
            state[1] -= 1
        elif action == 4:  # +z
            state[2] += 1
        elif action == 5:  # -z
            state[2] -= 1

        s_ = [{'X': state[0], 'Y': state[1], 'Z': state[2], 'C':state[3]}]

        # csv 파일 작성하기_새로운 액션에 대한
        csv_dir = r"C:\Users\break\Downloads\RLop\RLoptistruct\Demo\demo_com_0514\demo_com.csv"
        field = ['X', 'Y', 'Z', 'C']
        with open(csv_dir, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writeheader()
            writer.writerows(s_)

        # fusion360 모델 생성
        fusion360_com.makeblock(self.dig)

    def get_state(self):
        try:
            # csv 파일 받아오기_state
            csv_dir = r"C:\Users\break\Downloads\RLop\RLoptistruct\Demo\demo_com_0514\demo_com.csv"
            with open(csv_dir, 'r') as f:
                reader = csv.DictReader(f)
                dict_list = []
                for elemt in reader:
                    dict_list.append(elemt)
            if dict_list == []:
                print("빈 리스트1")

            X = int(dict_list[0]['X'])
            Y = int(dict_list[0]['Y'])
            Z = int(dict_list[0]['Z'])
            C = int(dict_list[0]['C'])
            # state설정
            state = [X, Y, Z, C]

            if len(state) == 4:
                # self loop return
                return state
            else:
                self.get_state()

        except:
            self.get_state()



