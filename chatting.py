from openai import OpenAI
from humanoid import Humanoid
import math
import os
import time
import sys

class HumanoidController:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.instruction = """
        당신은 사람 모형을 움직이는 AI입니다. 다음은 사람 모형을 움직이기 위한 설명서입니다.
        - 명령어는 모두 Python의 리스트에 담는 형식으로 하세요.
        1. 동작을 수행할 부위를 선택하세요.
        - 사람 모형은 left_arm, right_arm, left_leg, right_leg로 이루어져있습니다.
         이 모형을 움직이기 위해서 각각의 이니셜중 방향을 입력하고, 부위를입력합니다
        ex) 
        l
        a
        - 이 명령은 l(Left) a(Arm)을 움직이라는 명령어입니다.
        2. 어떻게 부위를 움직일지 정하세요.
        - 각도를 입력하고, 초를 입력하면 선택한 부위가 그만큼 움직입니다.
        ex)
        60
        0.3
        - 이 명령은 선택한 부위를 60도만큼 0.3초만에 움직이라는 명령입니다.
        종합하면 한 명령을 실행할때 다음과같은 형식이 됩니다.
        [ ["l", "a", 60, 0.3] ]
        다음 명령어는 Left_arm을 60도만큼 0.3만에 움직이라는 명령이됩니다.
        여러번 입력하고싶으면 뒤에 다른 명령어를 추가하세요.
        ex) [ ["l", "a", 60, 0.3],  ["l", "a", 50, 0.2] ]
        최종적으로 다음과같이 명령을 내릴수 있습니다.
        ex)
        [  ["l", "l", 60, 1],  ["l", "a", 50, 0.2],  ["l", "l", 60, 1],  ["l", "a", 50, 0.2] ]
        한번 한 동작은 끝까지 유지되므로 동작을 시행한 후 다시 모형을 원위치 시키세요. << 매우중요
        다리를 120도 이상 돌리거나 팔을 60도이상 돌리면 다른 부위와 겹칠수 있으니 주의하세요.
        모든 질문에는 반드시 명령어로 대답하세요. 다른 대답은 절대 허용되지 않습니다.
        인사와 같은 질문을 받으면 한쪽 손만 위아래로 흔들어 인사하는 동작을 하세요.
        ex) [["l", "a", 60, 0.5] ["l", "a", -60, 0.5]]
        """
        self.humanoid = Humanoid()

    def get_answer(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=1.5,
            max_tokens=1600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()

    def execute_commands(self, command_list):
        for command in command_list:
            arm_choice, move_joint, angle, duration = command
            joint_name = ('left_arm' if arm_choice == 'l' and move_joint == 'a' else
                          'right_arm' if arm_choice == 'r' and move_joint == 'a' else
                          'left_leg' if arm_choice == 'l' and move_joint == 'l' else
                          'right_leg')
            target_angle = angle * (math.pi / 180) 
            self.humanoid.move_joint(joint_name, target_angle, duration)
            self.humanoid.reset_position()

    def chat(self):
        messages = [{"role": "system", "content": self.instruction}]
        print("AI 휴머노이드 프로그램을 시작합니다")
        print("사용방법: \n 1. 환경변수에 'OPENAI_API_KEY'라는 변수를 추가하고 api키를 입력하세요. \n 2. AI에게 행동을 명령해보세요. \n 3. 종료라고 입력시 종료됩니다.")
        while True:
            user_input = input("[사용자]: ")
            if user_input.lower() == '종료':
                break
            messages.append({"role": "user", "content": user_input})

            print("AI가 생각중...", end='\n', flush=True)
            
            response = self.get_answer(messages)
            
            messages.append({"role": "assistant", "content": response})
            try:
                command_list = eval(response)
                if isinstance(command_list, list):
                    self.execute_commands(command_list)
            except Exception as e:
                print(f"명령어 실행 오류: {e}")
