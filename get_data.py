from threading import Thread
from Spider import Spider
from DataProcessor import Processor

number_of_spider = 1
spider_men = []
usernames = []

processor = Processor("data.csv")

memCode = processor.filter(K=16, select=("MemberCode",))

usernames = [code[0].lower() + "+" for code in memCode]

total = len(usernames)


def gogo():
    while usernames:
        username = usernames.pop(0)
        print(f"[+] Getting {username}")
        Spider(username).run()


for i in range(number_of_spider):
    spider_men.append(Thread(target=gogo))

for spider_man in spider_men:
    spider_man.start()
