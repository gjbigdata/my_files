import time
import random


def step(banker_num,player_num,play_policy):
    #默认回报为0
    reward = 0
    #玩家策略为1 表示需要抽牌，其他值均为保持
    if play_policy == 1:
        player_num += random.randint(0,13)
        if player_num>=21:
            reward = -1
    #模拟庄家每次都抽牌的情况
    # banker_num += random.randint(0,13)+ random.randint(0,13)
    # if banker_num>=21:
    #     reward = 1
    return banker_num,player_num,reward

if __name__ == "__main__":
    bank_num = random.randint(0,10)
    print("庄家的牌是:",str(bank_num))
    player_num = random.randint(1,22)
    print("玩家家的牌是:",str(player_num))
    game_over_flag = False
    reward = 0
    while not game_over_flag:
        policy = int(input("请输入是否继续：1表示继续，不继续请输入任意值"))
        bank_num,player_num,current_reward = step(bank_num,player_num,policy)
        print("庄家的牌是:",str(bank_num))
        print("玩家家的牌是:",str(player_num))
        reward += current_reward
        if current_reward == -1:
            game_over_flag = True
        elif current_reward == 1:
            game_over_flag = True
    print(reward)

