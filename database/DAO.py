from database.DB_connect import DBConnect
from model.Gene import Gene


class DAO:

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllChromosomes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Chromosome
                    from genes
                    where Chromosome >0"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['Chromosome'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnectedGenes():
        """ Un arco collega due cromosomi diversi solo se i due cromosomi contengono due geni (uno per cromosoma)
         che compaiono (nello stesso ordine) nella tabella interactions. Si noti che, per ciascun cromosoma, possono
         esistere più geni, e ciascuno di essi potrebbe essere presente più volte (associato a function diverse)."""
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g1.GeneID as Gene1, g2.GeneID as Gene2, i.Expression_Corr
                    FROM genes g1, genes g2, interactions i 
                    where  g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2  
                    and g2.Chromosome != g1.Chromosome
                    and g2.Chromosome>0
                    and g1.Chromosome>0
                    group by g1.GeneID, g2.GeneID"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['Gene1'], row['Gene2'], row['Expression_Corr']))

        cursor.close()
        conn.close()
        return result
