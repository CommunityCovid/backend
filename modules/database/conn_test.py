from ConnectingPool import getConnectionPool

if __name__ == '__main__':
    connection_pool = getConnectionPool()
    conn = getConnectionPool().get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from langxin_community.residents limit 1')
    print(cursor.fetchone())
