import pandas as pd
class Week:
    def __init__(self,cur_robot,skilled=0):
        self.skilled=skilled
        self.cur_robot=cur_robot
        self.buy_op=0
        self.fresh_op=0
n =104

def initial_week():
    li =[]
    data=pd.read_excel("data.xlsx")
    print(data)
    for i in range(n):
        if i==0:
            li.append(Week(data.iloc[i//8,i%7],skilled=50))
        else:
            li.append(Week(data.iloc[i//8,i%7]))
    return li

def Buy_op(li):
    res = []
    print("the result of operator in question 3")
    for index, week in enumerate(li):
        if index % 8 == 0: print()

        print(week.buy_op, end=" ")
        res.append(week.buy_op)

    last_buy_week=3
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

    print()
    print("-------------------------------------")
    print("the result of operator in question 4")
    for index, num in enumerate(res):
        if index % 8 == 0: print()
        print(num, end=" ")
    print()
    print("-------------------------------------")

    return res

def main(loss =False):
    li = initial_week()

    # for week in li:
    #     print(week.cur_robot)

    for index,week in enumerate(li):


        cur_need_robot = week.cur_robot
        cur_skill = week.skilled
        print("cur_skilled ：",cur_skill)

        """当不是最后一周此时还要买"""
        if index<n-1:


            """下一周可以使用的操作手 为当前买的和这一周保养的"""
            if index>=1:
                week.buy_op = max(4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled-4*li[index-1].cur_robot, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op + li[index - 1].cur_robot * 4
            else:
                week.buy_op = max(4 * (li[index + 1].cur_robot + cur_need_robot) - week.skilled, 0)
                li[index + 1].skilled = cur_skill - cur_need_robot * 4 + week.buy_op

            """判断训练是否足够"""
            if index>=1 and li[index-1].cur_robot*4<week.buy_op // 10 + 1:
                print(f"week {index} is not enough for training robot")

        """带有损失"""
        if loss:
            week.cur_robot=int(0.9*week.cur_robot)
        Buy_op(li)




if __name__ =="__main__":
    main(loss=True)
