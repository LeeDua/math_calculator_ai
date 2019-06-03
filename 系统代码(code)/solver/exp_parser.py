

class Exp_parser():
    def __init__(self):
        self.index = 0

    def expression(self,list):
        length = len(list)
        sum = self.factor(list,length)
        if sum is None:
            return
        while (self.index < length):
            if (list[self.index]['structure'] == '+' or list[self.index]['structure'] == '-'):
                flag = list[self.index]['structure']
                self.index = self.index + 1
                if self.index >= length:
                    print("格式错误")
                    return

                temp = self.factor(list,length)
                if temp is None:
                    return
                if (flag == '+'):
                    sum = sum + temp
                else:
                    sum = sum - temp
            else:
                print("格式错误")
                return

        return sum


    def factor(self,list,length):
        product = 1
        if (list[self.index]['type'] == 2 or list[self.index]['structure'] =='(' or list[self.index]['structure']==')'):
            sss = list[self.index]['structure']
            if(sss == '(' or sss ==')'):
                product = 1
            else:
                product = list[self.index]['structure']
            self.index = self.index + 1
            while (self.index < length):
                if (list[self.index]['structure'] == 'times' or list[self.index]['structure'] == 'div' or list[self.index]['structure'] == 'f' or list[self.index]['structure']=='x'):
                    a = list[self.index]['structure']
                    if(a == 'times' or a=='x'):
                        flag = '*'
                    else:
                        flag = '/'
                    self.index = self.index + 1
                    if self.index < length:
                        g = list[self.index]['structure']
                        if(g=='(' or g==')'):
                            temp = 1
                        else:
                         temp = list[self.index]['structure']
                    else:
                        print("格式错误")
                        return
                    if (flag == '*'):
                        product = product * temp
                    else:
                        product = product / temp
                    self.index = self.index + 1
                elif (list[self.index]['structure'] == '+' or list[self.index]['structure'] == '-' or list[self.index]['structure']=='x'):
                    break
                else:
                    print("格式错误")
                    return

        else:
            print("格式错误")
            return
        return product