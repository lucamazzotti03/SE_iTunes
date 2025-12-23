from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, sum(t.milliseconds ) as durata
                    from album a, track t
                    where a.id = t.album_id 
                    group by a.id 
                    having sum(t.milliseconds) > %s"""

        cursor.execute(query, (durata*60*1000,))

        for row in cursor:
            result.append(Album(row["id"], row["title"], row["durata"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_playlist():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """ select pt.track_id, t.album_id, pt.playlist_id 
                    from track t, playlist_track pt 
                    where t.id = pt.track_id  """

        cursor.execute(query)
        dict = {}
        for row in cursor:
            playlist_id = int(row["playlist_id"])
            album_id = int(row["album_id"])
            if playlist_id not in dict:
                dict[playlist_id] = [album_id]
            elif playlist_id in dict and album_id not in dict[playlist_id]:
                dict[playlist_id].append(album_id)

        print(dict)

        cursor.close()
        conn.close()
        return dict