import pymysql


def open_connection():
    """
    打开数据库连接
    :return: connection 对象
    """
    config = {
        'user': 'root',  # 替换为你的 MySQL 用户名
        'password': '030308150518lg#',  # 替换为你的 MySQL 密码
        'host': 'localhost',  # 指定主机名和端口号
        'database': 'match',  # 替换为你的数据库名
    }

    try:
        connection = pymysql.connect(**config)
        if connection.open:
            print("成功连接到 MySQL 数据库！")
            return connection
    except pymysql.Error as err:
        print(f"连接 MySQL 数据库时出错: {err}")
        return None


def execute_query(connection, sql):
    """
    执行 SQL 查询
    :param connection: 数据库连接对象
    :param sql: SQL 查询语句
    :return: 查询结果
    """
    cursor = None
    results = None

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
    except pymysql.Error as err:
        print(f"执行 SQL 查询时出错: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        return results


def close_connection(connection):
    """
    关闭数据库连接
    :param connection: 数据库连接对象
    """
    if connection is not None and connection.open:
        connection.close()
        print("MySQL 数据库连接已关闭")


if __name__ == '__main__':
    sql = "SELECT 消息类型 FROM flight_data WHERE 信息要素 LIKE '%联合目标%'"
    connection = open_connection()
    result = execute_query(connection, sql)
    close_connection(connection)
    print(result)
