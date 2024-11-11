from datetime import datetime


def insert_video(conn, title, desc, classification_id, file_path, cover_path, status=0):
    try:
        with conn.cursor() as cursor:
            # 检查标题是否已存在
            check_sql = "SELECT id FROM v_video WHERE title = %s"
            cursor.execute(check_sql, (title,))
            result = cursor.fetchone()

            if result:
                # 如果标题存在，则执行更新操作
                video_id = result[0]
                update_sql = """UPDATE v_video 
                                SET `desc` = %s, classification_id = %s, file = %s, cover = %s, status = %s, create_time = %s
                                WHERE id = %s"""
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(update_sql,
                               (desc, classification_id, file_path, cover_path, status, create_time, video_id))
                print("Data updated successfully.")
            else:
                # 如果标题不存在，则执行插入操作
                insert_sql = """INSERT INTO v_video (title, `desc`, classification_id, file, cover, status, create_time) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(insert_sql, (title, desc, classification_id, file_path, cover_path, status, create_time))
                print("Data inserted successfully.")

        conn.commit()
    except pymysql.Error as e:
        print(f"Error inserting/updating data: {e}")


import pymysql


def get_classification_id(conn, title):
    try:
        with conn.cursor() as cursor:
            # 查询分类表中是否存在给定标题
            sql = "SELECT id FROM v_classification WHERE title = %s"
            cursor.execute(sql, (title,))
            result = cursor.fetchone()

            if result:
                # 如果标题存在，则返回对应的ID
                return result[0]
            else:
                # 如果标题不存在，则将其写入分类表，并返回新插入行的ID
                with conn.cursor() as inner_cursor:
                    insert_sql = "INSERT INTO v_classification (title) VALUES (%s)"
                    inner_cursor.execute(insert_sql, (title,))
                    conn.commit()
                    return inner_cursor.lastrowid
    except pymysql.Error as e:
        print(f"Error retrieving classification ID: {e}")


def get_conn():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='Admin1234!', database='video', charset='utf8mb4')
    return conn


def set_classification(title):
    # Example usage:
    conn = get_conn()
    classification_id = get_classification_id(conn, title)
    print("Classification ID:", classification_id)
    conn.close()
    return classification_id


def upload_video(title, desc, classification_id, file_path, cover_path, status=0):
    # Example usage:
    conn = get_conn()
    # insert_video(conn, "Sample Video", "This is a sample video description.", 1, "/path/to/video.mp4", "/path/to/cover.jpg")
    insert_video(conn, title, desc, classification_id, file_path, cover_path, status=0)

    conn.close()


if __name__ == '__main__':
    set_classification('xj')
