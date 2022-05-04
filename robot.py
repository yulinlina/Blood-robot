import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

n =104

class Week:
    def __init__(self,cur_robot,skilled=0,boat=0):
        self.skilled=skilled        # 当前可以使用的操作手
        self.maintain_op = 0        # 当前在保养的操作手
        self.buy_op = 0             # 当前需要购买的操作手
        self.train_op =0             # 当前正在训练的操作手

        self.cur_robot=cur_robot   # 当前需要的机器人

        self.boat = boat          # 当前可以使用的容器
        self.maintain_boat =0      # 当前在保养的容器

def initial_week():
    li =[]
    data=pd.read_excel("data.xlsx")
    """ 返回每周的结构，包含需要多少个机器人"""

    for i in range(n):
        if i==0:
            li.append(Week(data.iloc[i//8,i%8],skilled=50,boat=13))
        else:
            li.append(Week(data.iloc[i//8,i%8]))

    """读取正确"""
    """多增加一个空白周，避免边界判断"""
    li.append(Week(0))
    return li

def func(x,a,b):
    return a*x+b

def predict(li):
    x =range(0,n)
    popt, pcov = curve_fit(func, x, li)
    a,b = popt  # popt里面是拟合系数，
    y_vals = func(x, a, b)

    plot1 = plt.plot(x, li,y_vals, '-', label='original values')

    plt.show()

    x_pre=range(105,112)
    y_pre=[a*x+b for x in x_pre]
    print(y_pre)

def week_buy_op(li):
    """返回每周购买的操作手"""
    li = []
    # print("the liult of operator in question 3")
    for index, week in enumerate(li):
        if index % 8 == 0: print()

        print(week.buy_op, end=" ")
        li.append(week.buy_op)

    return li

def question4(res,li, train_rate = 20, loss = 0.9):
    last_buy_week=3
    maintain_op = []
    boat =[]

    for index,week in enumerate(li):

        if not week.buy_op or index==0:li[index].buy_op=li[index].buy_op

        elif li[last_buy_week].buy_op>=40:
            if (index-last_buy_week)*5<=20:
                li[index].buy_op=0
                li[last_buy_week].buy_op+=week.buy_op
            else:
                last_buy_week=index

        elif 20<=li[last_buy_week].buy_op<40:
            """如果提前购买和当前求和能超过40"""
            if li[last_buy_week].buy_op+week.buy_op>=40:
                gap = 40-li[last_buy_week].buy_op
                if gap*10+(week.buy_op-gap)*20>=week.buy_op*5*(index-last_buy_week):
                    li[index].buy_op = 0
                    li[last_buy_week].buy_op += week.buy_op
                else:
                    last_buy_week = index
            #
            elif  li[last_buy_week].buy_op+week.buy_op<40:
                if week.buy_op*10>=week.buy_op*5*(index-last_buy_week):
                    li[index].buy_op = 0
                    li[last_buy_week].buy_op += week.buy_op
                else:
                    last_buy_week = index
        else:
           """如果上一次购买的操作手数量小于20"""
           if  week.buy_op>=40:
               if li[last_buy_week].buy_op*20>=week.buy_op*5*1:
                   li[index].buy_op = 0
                   li[last_buy_week].buy_op += week.buy_op
               else:
                   last_buy_week = index

           elif week.buy_op+li[last_buy_week].buy_op<20:
               last_buy_week = index

           elif week.buy_op+li[last_buy_week].buy_op<=40:
                gap=20-li[last_buy_week].buy_op
                if  (week.buy_op-gap)*10>= 5*week.buy_op*(index-last_buy_week):
                    li[index].buy_op = 0
                    li[last_buy_week].buy_op += week.buy_op
                else:
                    last_buy_week = index

        """当不是空白周，此时还要买操作手和容器艇"""
        cur_need_robot = week.cur_robot
        cur_skill = week.skilled

        if index < n:
            if index >= 1:
                """这周购买的操作手 =下周可用的 - 下周需要的血管操作手"""
                week.buy_op = max(
                    4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled - 4 * li[index - 1].cur_robot, 0)

                """购买了操作手进行训练,因为上一周的补给,判断一下是否训练足够"""
                if week.buy_op == 0:
                    week.train_op = 0
                elif week.skilled - 4 * cur_need_robot < week.buy_op // train_rate + 1:
                    gap = week.buy_op // train_rate + 1 - week.skilled + 4 * cur_need_robot
                    print(
                        f"week {index} is not enough for training robot，the gap is{gap},last week remaining is{li[index - 1].skilled - 4 * li[index - 1].cur_robot}")
                    # li[index - 1].buy_op += gap
                    # li[index].buy_op += gap
                    # week.train_op = week.buy_op // train_rate + 1
                else:
                    week.train_op = week.buy_op // train_rate + 1

                """下一周的可以使用操作手 =  这周剩余+这周购买+上周剩余"""
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op + li[index - 1].cur_robot * 4

                """购买容器艇 ,容器艇可以一直用"""
                li[index].boat = li[index - 1].boat
                """判断下一周容器是否够用"""
                if li[index].boat < li[index + 1].cur_robot:
                    gap = li[index + 1].cur_robot - li[index].boat
                    boat.append(gap)
                    li[index].boat += gap

                else:
                    """当前周保养容器"""
                    week.maintain_boat = li[index].boat - li[index].cur_robot
                    boat.append(0)

                """保养的操作手 = 上一周使用，这一周没有使用"""
                maintain_op.append(
                    li[index - 1].cur_robot * 4 + cur_skill - cur_need_robot * 4 - (li[index].buy_op // train_rate + 1))



            else:  # 第一周的操作手没有补给
                week.buy_op = max(4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op
                maintain_op.append(cur_skill - cur_need_robot * 4 - (week.buy_op // train_rate + 1))
                """第一周不需要买容器"""
                boat.append(0)
                week.train_op = week.buy_op // train_rate + 1

        """带有损失"""
        if loss:
            week.cur_robot = int(loss * week.cur_robot + 0.5)




    print()
    print("-------------------------------------")
    print("每周购买的操作手")
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        print(week.buy_op, end=" ")
    print()
    print("-------------------------------------")

    """保养的操作手"""
    print("每周保养的操作手")
    for index, week in enumerate(maintain_op):
        if index % 8 == 0: print()
        print(week, end=" ")
    print()
    print("每周保养的容器")
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        print(week.maintain_boat, end=" ")

    print()

    print("总成本：")
    sum = 0
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        if week.buy_op>40:
           op_money = (week.buy_op-40)*80+20*90+20*100
        elif 20<week.buy_op<=40:
           op_money = (week.buy_op - 20) * 90 + 20 * 100
        else:
           op_money=week.buy_op*100
        tem = op_money +week.boat*200 + week.maintain_boat * 10 + week.maintain_op * 5 + week.train_op * 10
        print(tem, end=" ")
        sum += tem
    print(f"总成本为{sum}")



def question2And3(li,loss =0.8,train_rate=10):
    maintain_op=[]
    boat =[]
    for index, week in enumerate(li):

        cur_need_robot = week.cur_robot
        cur_skill = week.skilled
        # print("cur_skilled ：", cur_skill)

        """当不是空白周，此时还要买操作手和容器艇"""
        if index < n:

            if index >= 1:
                """这周购买的操作手 =下周可用的 - 下周需要的血管操作手"""
                week.buy_op = max(
                    4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled - 4 * li[index - 1].cur_robot, 0)



                """购买了操作手进行训练,因为上一周的补给,判断一下是否训练足够"""
                if week.buy_op==0:
                    week.train_op=0
                elif week.skilled-4*cur_need_robot<week.buy_op//train_rate+1:
                    gap = week.buy_op//train_rate+1-week.skilled+4*cur_need_robot
                    print(f"week {index} is not enough for training robot，the gap is{gap},last week remaining is{li[index-1].skilled-4*li[index-1].cur_robot}")
                    li[index-1].buy_op+=gap
                    li[index].buy_op+=gap
                    week.train_op = week.buy_op // train_rate + 1
                else:
                    week.train_op = week.buy_op//train_rate+1

                """下一周的可以使用操作手 =  这周剩余+这周购买+上周剩余"""
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op + li[index - 1].cur_robot * 4

                """购买容器艇 ,容器艇可以一直用"""
                li[index].boat = li[index - 1].boat
                """判断下一周容器是否够用"""
                if li[index].boat < li[index+1].cur_robot:
                    gap = li[index+1].cur_robot - li[index].boat
                    boat.append(gap)
                    li[index].boat += gap

                else:
                    """当前周保养容器"""
                    week.maintain_boat=li[index].boat-li[index].cur_robot
                    boat.append(0)


                """保养的操作手 = 上一周使用，这一周没有使用"""
                maintain_op.append(li[index-1].cur_robot*4+cur_skill - cur_need_robot * 4-(li[index].buy_op//train_rate+1))



            else: # 第一周的操作手没有补给
                week.buy_op = max(4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op
                maintain_op.append(cur_skill - cur_need_robot * 4-(week.buy_op//train_rate+1))
                """第一周不需要买容器"""
                boat.append(0)
                week.train_op=week.buy_op//train_rate+1

        """带有损失"""
        if loss:
            week.cur_robot = int(loss * week.cur_robot+0.5)


    """最后一周的不需要买容器"""
    boat.append(0)

    """购买的操作手"""
    print("每周购买的操作手")
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        print(week.buy_op, end=" ")
    print()
    """保养的操作手"""
    print("每周保养的操作手")
    for index, week in enumerate(maintain_op):
        if index % 8 == 0: print()
        print(week, end=" ")

    print()
    print("每周购买的容器")
    for index, week in enumerate(boat):
        if index % 8 == 0: print()
        print(week, end=" ")

    print()

    print()
    print("每周保养的容器")
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        print(week.maintain_boat, end=" ")

    print()

    print("总成本：")
    sum = 0
    for index, week in enumerate(li):
        if index % 8 == 0: print()
        tem = week.buy_op*100+week.boat*200+week.maintain_boat*10+week.maintain_op*5+week.train_op*10
        print(tem, end=" ")
        sum+=tem
    print(f"总成本为{sum}")
    print()

    res = week_buy_op(li)
    return res,li




def main(pred=False):
    li = initial_week()

    if pred:
        robot =[]
        for week in li:
            robot.append(week.cur_robot)
        predict((robot))
    # for week in li[1:16]:
    #     print(week.cur_robot)

    res,li = question2And3(li,loss=0.9,train_rate=20)
    # print(len(li))
    question4(res,li)








if __name__ =="__main__":
    main()
