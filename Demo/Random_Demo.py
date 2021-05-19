import pandas as pd
import random


def random_point(nline:int, npoint:int):
        lines = []
        endpoints = []
        for i in range(nline):
            end_point = random.randrange(0, npoint)
            lines.append('Line{}'.format(i))
            endpoints.append(end_point)

        data = {'Line_num': lines,
                'end_point': endpoints}
        df = pd.DataFrame(data)
        df.set_index('Line_num', inplace=True)
        print(df)
        df.to_csv(r"C:\Users\break\Downloads\test\text.csv")


random_point(5,9)
        # rad_point1 = random.randrange(1,4)
        # rad_point2 = random.randrange(1,4)
        # rad_point3 = random.randrange(1,4)
        #
        # data = {'Line_num': ['Line1', 'Line2', 'Line3'],
        #         'end_point' : [rad_point1, rad_point2, rad_point3]}
        #
        # df = pd.DataFrame(data)
        # df.set_index('Line_num', inplace=True)
        # print(df)
        #
        # df.to_csv(r"C:\Users\break\Downloads\test\text.csv")

