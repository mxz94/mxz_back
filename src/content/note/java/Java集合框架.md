---
pubDatetime: 2023-12-12T16:00:00Z
title: Java集合框架
slug: Java集合框架
tags:
  - "java"
---

# 一. 集合

ArrayList 默认初始容量10 内部数组对象存储 扩容为当前容量的1.5倍 排序采用快排

HashMap 默认初始16 负载因子0.75 扩容为当前容量的2倍 采用链表+红黑树 链表长度大于8转为红黑树 小于6转为链表, computeIfAbsent value 不为null 进行计算赋值 computeIfPresent 为null 删除， 不为null 替换， compute 不为null替换， 为null 新增

ConcurrentHashMap 先cas 不成功说明位置已被抢占，此时那当前根节点（也就是桶）加锁，往后面续

HashSet 内部保存了一个HashMap 存储的key为保存的值。value是一个没用的对象

ArrayDeque 初始大小16 扩容为当前容量的2倍 采用数组存储 采用头尾指针 头尾指针相遇时扩容为当前容量的2倍

ArrayBlockingQueue add(加不进去抛异常) offer(加不进去false) put(加不进去阻塞) 内部一把锁， 两个condition (notFull 和 notEmpty) 互相唤醒 放满 唤醒notEmpty, 取走一个就唤醒notFull, 一次只唤醒一个等待的condition

LinkedBlockingQueue 双锁读写分离， 因为他是链表， 所以读写可以不用同一把锁, put， 达到最大容量wait， 唤醒一个等待线程，如果还小继续唤醒，结束的时候判断是count 是否为0， 如果为0， 则代表新增了一个，唤醒一个take线程

DelayQueue  指定时间才能获得

CopyOnWriteArrayList add 加锁复制一份， 此时get 不受影响，读取的是复制的array

ConcurrentLinkedDeque cas 插入链表不进行阻塞