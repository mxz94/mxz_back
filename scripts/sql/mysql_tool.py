
import logging
import warnings
import pymysql
warnings.simplefilter("ignore")
_logger = logging.getLogger(__name__)

class my_mysql():
    driver = pymysql
    """The my_mysql is a tool for mysql connect."""

    def __init__(self, host, user, database, password, port=3306, default_character_set="utf-8"):
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        self.port = port
        self.default_character_set = default_character_set

    def _connect(self):
        try:
            return self.driver.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                       db=self.database, charset='utf8')
        except AttributeError:
            _logger.error("No connect method found in self.driver module")

    def my_fetchall(self, sql, args=None, return_type=None):
        rows = []
        try:
            con = self._connect()
            if return_type == "dict":
                cur = con.cursor(self.driver.cursors.DictCursor)
            else:
                cur = con.cursor()
            try:
                if ";" not in sql:
                    _logger.warning('mysql_toool.my_fetchall: sql not end with \";\";')
                cur.execute(sql, args)
                rows = cur.fetchall()
                rows = [r for r in rows]
                print("my_fetchall sql is %s" % cur._executed)
                _logger.debug("dmy_fetchall sql is %s" % cur._executed)
            except self.driver.Error as error:
                _logger.error('mysql_toool.my_fetchall: sql:' + sql +';'+ str(error))
            finally:
                con.close()
        except self.driver.Error as error:
            _logger.error('mysql_toool.my_fetchall: default.cnf error:' + str(error))
        if str(rows) == "[(None,)]":
            rows = []
        return rows


    def my_fetchone(self, sql, args=None, return_type=None):
        row = []
        try:
            con = self._connect()
            if return_type == "dict":
                cur = con.cursor(self.driver.cursors.DictCursor)
            else:
                cur = con.cursor()
            try:
                if ";" not in sql:
                    _logger.warning('mysql_toool.my_fetchone: sql not end with \";\";')
                cur.execute(sql, args)
                row = cur.fetchone()
                print(cur._executed)
                _logger.info("my_fetchone sql is %s" % cur._executed)
            except self.driver.Error as error:
                smb("fetch one error: sql = %s ; error= %s" % (cur._last_executed, str(error)))
                _logger.error("mysql_toool.my_fetchone: sql = %s ; error= %s" % (cur._last_executed, str(error)))
                raise error
            finally:
                con.close()
        except self.driver.Error as error:
            _logger.error('mysql_toool.my_fetchone: default.cnf error:' + str(error))
        if row is None:
            row = []
        if str(row) == "(None,)":
            row = []
        return row

    def my_fetchone_new(self, sql_list, args=None, return_type=None):
        row_list = []
        try:
            con = self._connect()
            if return_type == "dict":
                cur = con.cursor(self.driver.cursors.DictCursor)
            else:
                cur = con.cursor()

            for sql in sql_list:
                if ";" not in sql:
                    _logger.warning('mysql_toool.my_fetchone: sql not end with \";\";')
                try:
                    cur.execute(sql, args)
                    row = cur.fetchone()
                    row_list.append(row)
                    _logger.info("my_fetchone_new sql is %s" % cur._executed)
                except self.driver.Error as error:
                    _logger.error('mysql_toool.my_fetchone: sql:' + str(error))
                    con.close()
                    break
            try:
                con.close()
            except Exception as e:
                pass
        except self.driver.Error as error:
            _logger.error('mysql_toool.my_fetchone: default.cnf error:' + str(error))
        return row_list

    def exe_update(self, table, colomns, conditions):
        """

        :param table: 表名
        :param colomns: 更新列
        :param conditions: 条件
        :return:
        """
        handled_item = 0
        try:
            con = self._connect()
            cur = con.cursor()
            try:
                sql = "update {} set ".format(table)
                cols = []
                vals = []
                for k, v in colomns.items():
                    if v is not None:
                        if v == "now()":
                            col = "{}=now()".format(k)
                            cols.append(col)
                        else:
                            col = "{}=%s".format(k)
                            cols.append(col)
                            vals.append(v)
                cons = []
                for k, v in conditions.items():
                    wheres = "{}=%s".format(k)
                    cons.append(wheres)
                    vals.append(v)

                sql = "{} {} where {};".format(sql, ",".join(cols), ",".join(cons))
                print(sql)

                handled_item = cur.execute(sql, vals)
                _logger.debug("execute sql is %s" % cur._executed)
            except self.driver.Error as error:
                _logger.error('mysql_toool.execute except: sql:' + sql + ';\n'+ str(error))
                return -1
            finally:
                con.commit()
                con.close()
        except Exception as error:
            _logger.error('mysql_toool.execute: default.cnf error:' + sql + ';'+ str(error))
            return -1
        return handled_item

    def execute(self, sql, args=None):
        """

        :param sql: type must be str.
            if update success, return count of update rows.
            if delete success, return count of delete rows.
            if insert success, return 1.
            else return 0.

        :return:
        """
        handled_item = 0
        try:
            con = self._connect()
            cur = con.cursor()
            try:
                if ";" not in sql:
                    _logger.warning('mysql_toool.execute: sql not end with \";\";')
                handled_item = cur.execute(sql, args)
                _logger.error("execute sql is %s" % cur._executed)
            except self.driver.Error as error:
                _logger.error('mysql_toool.execute except: sql:' + sql + ';\n'+ str(error))
                return -1
            except Exception as error:
                _logger.error('mysql_toool.execute except: sql:' + sql + ';\n' + str(error))
            finally:
                con.commit()
                con.close()
        except Exception as error:
            _logger.error('mysql_toool.execute: default.cnf error:' + sql + ';'+ str(error))
            return -1
        return handled_item

    def insert(self, sql, args=None):
        """
        insert action
        :return:
        """
        handled_item = 0
        try:
            con = self._connect()
            cur = con.cursor()
            try:
                cur.execute(sql, args)
                handled_item = cur.lastrowid
                _logger.info("insert sql is %s" % cur._executed)
            except self.driver.Error as error:
                _logger.error('mysql_toool.execute: sql:' + sql+str(error))
            finally:
                con.commit()
                con.close()
        except self.driver.Error as error:
            _logger.error('mysql_toool.execute: default.cnf error:' + str(error))
        return handled_item

    def execute_transaction(self, array_sql_action, args=None):
        """

        :param array_sql_action:
            The format is a single SQL, or list ﹣ SQL
        All the list SQL executed successfully, return len (list_sql)
        :return:
        """
        handled_item = 0
        try:
            con = self._connect()
            cur = con.cursor()
            sql = ""
            try:
                con.autocommit(False)
                if type(array_sql_action) is list:
                    i = 1
                    for item in array_sql_action:
                        sql = item
                        if ";" not in sql:
                            _logger.warning('mysql_toool.execute_transaction: sql not end with \";\";')
                        if args is not None:
                            handled_item = handled_item + cur.execute(sql, args[i-1])
                        else:
                            handled_item = handled_item + cur.execute(sql)
                        _logger.info("execute_transaction sql %s is %s" % (i, cur._executed))
                        i = i + 1
                else:
                    handled_item = cur.execute(array_sql_action)
            except self.driver.Error as error:
                handled_item = -1
                con.rollback()
                _logger.error('mysql_toool.execute_transaction: sql: %s : %s' % (sql, str(error)))
            finally:
                con.commit()
                con.close()
        except self.driver.Error as error:
            _logger.error('mysql_toool.execute_transaction: default.cnf error:' + str(error))
        return handled_item

