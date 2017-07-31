class ATest111:
    count=0
    def aaa(self):
        print(ATest111.count)


if __name__ == '__main__':
    for i in range(100):
        ATest111.count+=1
    print(ATest111.count)