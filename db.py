import psycopg2


def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname='vedas',
            user='postgres',
            password='sac123',
            host='localhost',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None



def get_pool_details():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
         
            query = """
                SELECT p.pool_name, 
                       SUM(d.capacity) AS total_capacity, 
                       SUM(d.usage) AS used_space, 
                       SUM(d.capacity - d.usage) AS free_space
                FROM pool p
                JOIN disks d ON p.pool_id = d.pool_id where type='master'
                GROUP BY p.pool_name
            """
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            cursor.close()
            conn.close()
     
            return [
                {
                    'pool_name': row[0], 
                    'capacity': row[1], 
                    'used_space': row[2], 
                    'free_space': row[3]
                } for row in result
            ]
        except psycopg2.DatabaseError as e:
            print(f"Database query error: {e}")
            return []
    else:
        return []


def get_slave_details(pool_name):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT d.disk_name, d.capacity,d.usage, (d.capacity - d.usage) AS free_space
                FROM disks d
                JOIN pool p ON d.pool_id = p.pool_id
                WHERE p.pool_name = %s AND d.type = 'slaves'
            """
            cursor.execute(query, (pool_name,))
            result = cursor.fetchall()
            print("slaves",result)
            cursor.close()
            conn.close()
            return [
                {
                    'disk_name': row[0], 
                    'capacity': row[1],
                    'usage':row[2] ,
                    'free_space': row[3]
                } for row in result
            ]
        except psycopg2.DatabaseError as e:
            print(f"Database query error: {e}")
            return []
    else:
        return []