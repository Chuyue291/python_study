from typing import Self


class Questionnaire:
    def __init__(self, title, qaa: list[list[tuple]]):
        # 初始化Questionnaire类，传入标题和问题答案列表
        self.qaa = qaa
        self.title = title
        self.question = [i[0] for i in qaa]
        self.answer = [i[1] for i in qaa]

    def __enter__(self):
        # 进入with语句时,打印问卷开始
        print(f"Questionnaire {self.title} start")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出with语句时,计算正确答案数,错误答案数,得分,总题数,用户答案列表
        right = 0
        wrong = 0
        score = 0
        total = len(self.question)
        user_answers = []

        # 遍历问题答案列表,获取用户答案,并判断答案是否正确
        for q, a in zip(self.question, self.answer):
            at = type(a)
            answer = at(input(f'Ask: {q}, answer: '))
            user_answers.append(answer)
            if answer == a:
                right += 1
                score += 1
                print("Right!")
            else:
                wrong += 1
                score = max(score - 1,0)
                print("Wrong!")

        # 计算正确率,错误率
        AP = 0 if total == 0 else ((right / total) * 100 if total != 0 else 0)
        WP = 0 if total == 0 else ((wrong / total) * 100 if total != 0 else 0)
        # 打印问卷结束,正确答案数,错误答案数,得分,正确率,错误率,正确答案列表,用户答案列表
        print(f"Questionnaire {self.title} end, right: {right}, wrong: {wrong}, score: {score}")
        print(f"AP: {AP}%, WP: {WP}%")
        print(f"right answers: {str(self.answer)[1:-1]}, your answers: {str(user_answers)[1:-1]}")


# 使用with语句创建Questionnaire对象,传入标题和问题答案列表
with Questionnaire('title', [['1+1', 2], ['9-8', 1]]):
    pass
