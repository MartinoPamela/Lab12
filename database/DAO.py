from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.dailySale import DailySale
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_daily_sales gds"""

        cursor.execute(query)

        for row in cursor:
            result.append(DailySale(row["Retailer_code"], row["Product_number"], row["Order_method_code"],
                                    row["Date"], row["Quantity"], row["Unit_price"], row["Unit_sale_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(gr.Country)
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year, country, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gr.Retailer_code as r1, gr2.Retailer_code as r2, count(distinct gds.Product_number) as N
                    from go_daily_sales gds, go_daily_sales gds2, go_retailers gr, go_retailers gr2  
                    where year(gds.`Date`) = year(gds2.`Date`)
                    and year(gds.`Date`) = %s
                    and gr.Country = %s
                    and gr2.Country = %s
                    and gr.Retailer_code != gr2.Retailer_code
                    and gds.Product_number = gds2.Product_number 
                    and gr.Retailer_code = gds.Retailer_code
                    and gr2.Retailer_code = gds2.Retailer_code
                    group by gr.Retailer_code, gr2.Retailer_code"""

        cursor.execute(query, (str(year), country, country))

        for row in cursor:
            result.append(Connessione(idMap[row["r1"]], idMap[row["r2"]], row["N"]))

        cursor.close()
        conn.close()
        return result
