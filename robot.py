import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class Week:
    def __init__(self,cur_robot,skilled=0,boat=0):
        self.skilled=skilled
        self.cur_robot=cur_robot
        self.buy_op=0
        self.fresh_op=0
        self.boat = boat
n =104

def initial_week():
    li =[]
    data=pd.read_excel("data.xlsx")
    print(data)
    for i in range(n):
        if i==0:
            li.append(Week(data.iloc[i//8,i%7],skilled=50,boat=13))
        else:
            li.append(Week(data.iloc[i//8,i%7]))
    return li

def func(x,a,b):
    return a*x+b

def predict(res):
    x =range(0,n)
    popt, pcov = curve_fit(func, x, res)
    a,b = popt  # popt里面是拟合系数，读者可以自己help其用法
    y_vals = func(x, a, b)

    plot1 = plt.plot(x, res,y_vals, '-', label='original values')

    plt.show()

    x_pre=range(105,112)
    y_pre=[a*x+b for x in x_pre]
    print(y_pre)

def Buy_op(li):
    res = []
    print("the result of operator in question 3")
    for index, week in enumerate(li):
        if index % 8 == 0: print()

        print(week.buy_op, end=" ")
        res.append(week.buy_op)

    return res

def question4(res,li):
    last_buy_week=3
    maintain_op = []

    for index,num in enumerate(res):

        if not num or index==0:continue


        if res[last_buy_week]>=40:
            if (index-last_buy_week)*5<=20:
                res[index]=0
                res[last_buy_week]+=num
            else:
                last_buy_week=index

        if 20<=res[last_buy_week]<40:
            """如果提前购买和当前求和能超过40"""
            if res[last_buy_week]+num>=40:
                gap = 40-res[last_buy_week]
                if gap*10+(num-gap)*20>=num*5*(index-last_buy_week):
                    res[index] = 0
                    res[last_buy_week] += num
                else:
                    last_buy_week = index
            #
            elif  res[last_buy_week]+num<40:
                if num*10>=num*5*(index-last_buy_week):
                    res[index] = 0
                    res[last_buy_week] += num
                else:
                    last_buy_week = index

        if res[last_buy_week]<20:
           if  num>=40:
               if res[last_buy_week]*20>=num*5*1:
                   res[index] = 0
                   res[last_buy_week] += num
               else:
                   last_buy_week = index

           elif num+res[last_buy_week]<20:
               last_buy_week = index

           elif num+res[last_buy_week]<=40:
                gap=20-res[last_buy_week]
                if  (num-gap)*10>= 5*num*(index-last_buy_week):
                    res[index] = 0
                    res[last_buy_week] += num
                else:
                    last_buy_week = index

    """保养的操作手 = 上一周使+(可用-这一周需要使用-这一周训练)"""

    for index,week in enumerate(li):
        loss =0.9
        if index<n-1:
            week.buy_op=res[index]
            cur_skill = week.skilled
            cur_need_robot = week.cur_robot

            if index >= 1:
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op + li[index - 1].cur_robot * 4
                maintain_op.append(
                li[index - 1].cur_robot * 4 + cur_skill - cur_need_robot * 4 - (week.buy_op // 10 + 1))
            else:
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op
                maintain_op.append(cur_skill - cur_need_robot * 4 - (week.buy_op // 10 + 1))
        if loss:
            week.cur_robot = int(loss * week.cur_robot)

    print()
    print("-------------------------------------")
    print("the result of operator in question 4")
    for index, num in enumerate(res):
        if index % 8 == 0: print()
        print(num, end=" ")
    print()
    print("-------------------------------------")

    """保养的操作手"""
    print("每周保养的操作手")
    for index, num in enumerate(maintain_op):
        if index % 8 == 0: print()
        print(num, end=" ")



def question2And3(li,loss =0.8):
    maintain_op=[]
    boat =[]

    for index, week in enumerate(li):

        cur_need_robot = week.cur_robot
        cur_skill = week.skilled
        # print("cur_skilled ：", cur_skill)

        """当不是最后一周此时还要买"""
        if index < n - 1:

            """下一周可以使用的操作手 为当前买的和这一周保养的"""
            if index >= 1:
                week.buy_op = max(
                    4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled - 4 * li[index - 1].cur_robot, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op + li[index - 1].cur_robot * 4
                # 保养的操作手 = 上一周使用，这一周没有使用
                maintain_op.append(li[index-1].cur_robot*4+cur_skill - cur_need_robot * 4-(week.buy_op//10+1))

                """购买容器艇 ,容器艇可以一直用"""
                li[index].boat=li[index-1].boat
                if  li[index].boat<li[index].cur_robot:
                    gap = li[index].cur_robot-li[index].boat
                    boat.append(gap)
                    li[index].boat+= gap
                else:
                    boat.append(0)

            else:
                week.buy_op = max(4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op
                maintain_op.append(cur_skill - cur_need_robot * 4-(week.buy_op//10+1))

            """判断训练是否足够"""
            if index >= 1 and li[index - 1].cur_robot * 4 < week.buy_op // 10 + 1:
                print(f"week {index} is not enough for training robot")



        """带有损失"""
        if loss:
            week.cur_robot = int(loss * week.cur_robot)
    """保养的操作手"""
    print("每周保养的操作手")
    for index, num in enumerate(maintain_op):
        if index % 8 == 0: print()
        print(num, end=" ")

    print()
    print("每周购买的容器")
    for index, num in enumerate(boat):
        if index % 8 == 0: print()
        print(num, end=" ")

    print()
    res = Buy_op(li)
    return res,li




def main(pred=False):
    li = initial_week()

    if pred:
        robot =[]
        for week in li:
            robot.append(week.cur_robot)
        predict((robot))

    res,li = question2And3(li,loss=0.9)

    question4(res,initial_week())








if __name__ =="__main__":
    main()
