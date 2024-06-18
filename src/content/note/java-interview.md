---
pubDatetime: 2024-06-18 16:58:08
title: java-interview
slug: java-interview
tags:
- "java"
---

# MYSQL
1. 脏读：读取到未提交的数据, 不可重复读：读取一次数据后，被修改，再读改变了  幻读：两次读的条数不一致，   丢失修改
2. Read Uncommitted(没解决)  READ COMMITTED(无脏读， 读写分离锁) REPEATABLE READ(脏  幻， B事务 不会修改A事务读取到的未提交事务的快照数据   默认 )  Serializable(全解决，表锁) 
3. spring 事务传播级别 1. REQUIRED(重入锁) 2. SUPPORTS 3. MANDATORY 4. REQUIRES_NEW 5. NOT_SUPPORTED 6. NEVER
4. explain
   1. | 字段名        | 含义                                                         |
      |---------------|------------------------------------------------------------|
      | `id`          | 执行编号 值越大越先执行                                               |
      | `select_type` | 查询类型，如 SIMPLE（简单查询），PRIMARY（主查询），SUBQUERY（子查询），UNION 等。    |
      | `table`       | 查询操作涉及的表。                                                  |
      | `partitions`  | 查询扫描的分区。                                                   |
      | `type`        | 连接类型，如 ALL（全表扫描）、index（索引扫描）、range（范围扫描）等。                 |
      | `possible_keys` | 查询中可能使用的索引。                                                |
      | `key`         | 查询实际使用的索引。                                                 |
      | `key_len`     | 使用的索引的长度。                                                  |
      | `ref`         | 哪个列或常量与 key 一起用于从表中选择行。                                    |
      | `rows`        | 估计需要读取的行数。                                                 |
      | `filtered`    | 估计表的行数中满足查询条件的行百分比。                                        |
      | `Extra`       | 有关查询额外信息，如 Using temporary（使用临时表）、Using filesort（使用文件排序）等。 |
   2.  索引失效原因：1. 查询数量是大表的大部分 2. 索引 id+1 = 2 包含计算 3. 隐式转换 text = 1111333 失效 应该为 text = ‘1111333’ 4. like ‘%2121’ 5. not in ,not exist.
   3. 索引最左匹配原则
3. 如何挑选索引 数据大的列， 搜索的列 数据类型小 name[10]  主键自增
4. order by 字段相同时 会随机排序， 所以要再加id  
5. 数据库引擎  show engines;  主表 Innodb  从表 MYISAM(无事务， 主insert  select 有 count计数器)
6. 数据库事务ACID 原子性 一致性 隔离性 持久性
7. delete(条件删)  truncate(全删， 重置id主键) 
8. MVVC  多版本并发控制, 读写冲突的无锁并发控制，为每个修改保存一个版本。版本与事务时间戳关联，读操作只读该事务开始前的数据库的快照（复制了一份数据）。这样在读操作不用阻塞写操作，写操作不用阻塞读操作的同时，避免了脏读和不可重复读. 解决了脏幻不可重复
9. MVVC  实现原理主要是依赖记录中的 3 个隐式字段、undo 日志、Read View 来实现的 
10. MYSQL 中的锁
    1. 共享锁（S） 可多用户读
    2. 排他锁 写阻塞其他读和写
    3. 表锁 MYISAM
    4. 行锁 只能加在索引上，InnoDB有索引会行锁