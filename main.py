import sqlite3
import pyarrow.parquet as pq

database_name = "even_financial.db"


def main():
    table2 = pq.read_table('ds_offers.parquet.gzip')
    df = table2.to_pandas()
    print(df)
    print(df.info(verbose=True))
    conn = sqlite3.connect(database_name)
    df.to_sql(name="offers", con=conn, if_exists='replace', index=False)
    conn.commit()
    print("Offers data has been uploaded to sqlite table")


def main_2():
    table2 = pq.read_table('ds_leads.parquet.gzip')
    df = table2.to_pandas()
    print(df)
    print(df.info(verbose=True))
    conn = sqlite3.connect(database_name)
    df.to_sql(name="leads", con=conn, if_exists='replace', index=False)
    conn.commit()
    print("Leads data has been uploaded to sqlite table")


def main_3():
    table2 = pq.read_table('ds_clicks.parquet.gzip')
    df = table2.to_pandas()
    print(df)
    print(df.info(verbose=True))
    conn = sqlite3.connect(database_name)
    df.to_sql(name="clicks", con=conn, if_exists='replace', index=False)
    conn.commit()
    print("Clicks data has been uploaded to sqlite table")


if __name__ == '__main__':
    main()
    main_2()
    main_3()
