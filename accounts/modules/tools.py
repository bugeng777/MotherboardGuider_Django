# 随机产生（数字、字母）模块
class ProduceCode:
    # 定义一个空列表，是随机数来源的容器
    __rand_num = list()

    # 定义一个空集合，用于存储已经产生的验证码，（也可以用空列表）
    __abandon = set()

    # 验证码容器
    @classmethod
    def __vessel(cls, option='num or letter'):

        # 清空列表，（随机数来源的容器）
        cls.__rand_num = list()

        if option == 'num':
            # 把数字存入列表
            for i in range(10):
                cls.__rand_num.append(str(i))

        elif option == 'letter':
            # 把大小写字母存入列表
            for i in range(26):
                cls.__rand_num.append(chr(i + 65))  # 大写字母
                cls.__rand_num.append(chr(i + 97))  # 小写字母

        elif option == 'num or letter':
            # 把数字存入列表
            for i in range(10):
                cls.__rand_num.append(str(i))

            # 把大小写字母存入列表
            for i in range(26):
                cls.__rand_num.append(chr(i + 65))  # 大写字母
                cls.__rand_num.append(chr(i + 97))  # 小写字母

        else:
            print('参数option传递错误！！！')
            print("option='num' or 'letter'")

            import sys
            sys.exit()

    # 随机生成6位验证码
    @classmethod
    def auth_code(cls, option='num or letter', num=6):

        buf = ''  # 定义一个空的字符串，用于存储6位验证码

        cls.__vessel(option=option)  # 验证码容器

        from random import choice  # 导入随机模块

        for i in range(num):
            buf += choice(cls.__rand_num)  # 随机数拼接成6位验证码

        # 如果废弃站集合为空
        if cls.__abandon == set():
            cls.__abandon.add(buf)  # 把验证码存入废弃站集合，说明此验证码不能再使用
            return buf

        # 保证6位验证码不重复
        for i in cls.__abandon:

            # 如果验证码重复
            if buf == i:
                buf = cls.auth_code(option=option, num=num)
                return buf

        # 验证码不重复
        cls.__abandon.add(buf)  # 把验证码存入废弃站集合，说明此验证码不能再使用
        return buf

    # 查看数据
    @classmethod
    def check_data(cls):
        print(f'随机数库：{cls.__rand_num}')
        print('废弃站：{}'.format(cls.__abandon))

    # 清空废弃站
    @classmethod
    def clear_abandon(cls):
        cls.__abandon.clear()