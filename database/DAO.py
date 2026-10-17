from database.DB_connect import DBConnect
from model.circuit import Circuit
class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT distinct year FROM seasons s  "
                 "ORDER BY year")

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT c.circuitId AS id, c.circuitRef AS ref, c.name AS nome,
                       c.location AS loc, c.country AS country
                FROM circuits c, races r
                WHERE c.circuitId = r.circuitId AND r.year BETWEEN %s AND %s
                """
        cursor.execute(query, (anno1, anno2))
        for row in cursor:
            results.append(Circuit(row["id"], row["ref"], row["nome"], row["loc"], row["country"]))
        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getEdges(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            print("Connessione fallita")
            return results

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT r1.circuitId as id1, r2.circuitID as id2, COUNT(DISTINCT r1.year) AS peso
                FROM races r1, races r2
                WHERE r1.year = r2.year AND r2.round = r1.round+1
                AND r1.circuitId <> r2.circuitId
                AND r1.year BETWEEN %s AND %s
                GROUP BY r1.circuitId, r2.circuitId
                """
        cursor.execute(query, (anno1, anno2))
        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))
        cursor.close()
        conn.close()
        return results

