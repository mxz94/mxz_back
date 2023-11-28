import random


def insert_sort2(a : list):
    n = len(a)

    for i in range(1, n):
        insert = a[i]
        j = i - 1
        while (j >= 0 and a[j] > insert):
            j = j - 1

        # if j != i - 1:
        for k in range(i - 1, j, -1):
            a[k + 1] = a[k]
        a[j+1] = insert



# 插入排序
def insert_sort(a):
    n = len(a)

    for i in range(1, n):
        # 为 a[i] 在前面的 a[0...i-1] 有序区间中找一个合适的位置
        j = i-1
        while(j >= 0 and a[j] > a[i]):
            j -= 1
        # 如找到了一个合适的位置
        if j != i - 1:
            # 将比 a[i] 大的数据向后移
            temp = a[i]
            for k in range(i - 1, j, -1):
                a[k + 1] = a[k]
            # 将 a[i] 放到正确位置上
            a[j + 1] = temp
    return a

def select_sort(a : list):
    n = len(a)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if a[j] < a[min_index]:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a


if __name__ == '__main__':
    for i in range(10):
        print(random.randrange(0, 10))
    a = [3, 2, 4, 1, 5, 6, 7, 8, 9, 0]
    insert_sort2(a)
    print(a)
