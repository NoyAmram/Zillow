import pymysql
import zillow_config as cfg


def data_to_db(df):
    """Inserts specific columns from df, to the database zillow"""
    # connect to mysql using pymysql
    try:
        conn = pymysql.connect(user='root', password=cfg.SQL_PASS, database='zillow')
    except Exception as error:
        print(f'Below error occurred. Did you create the database? \n {error}')
        cursor = conn.cursor()
    # there are <0.5% data that has NaN. Fill them with 0 for easy process.
    df = df.fillna(0)
    # convert data type
    df['zpid'] = df['zpid'].astype(int)
    df['zestimate'] = df['zestimate'].astype(float)
    df['price'] = df['price'].map(lambda x: x[1:] if x[0] == '$' else x)
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].str.replace('+', '').astype(float)
    df['addressZipcode'] = df['addressZipcode'].astype(int)
    df['beds'] = df['beds'].astype(int)
    df['baths'] = df['baths'].astype(int)
    df['area'] = df['area'].astype(float)
    # select wanted columns from df and save into lists.
    house_units = df[['zpid', 'price', 'zestimate', 'statusText']].values.tolist()
    unit_images = df[['imgSrc']].values.tolist()
    unit_links = df[['detailUrl']].values.tolist()
    unit_addresses = df[['addressStreet', 'addressCity', 'addressState', 'addressZipcode']].values.tolist()
    unit_infos = df[['beds', 'baths', 'area']].values.tolist()
    # queries for inserting data
    q1 = "insert into house_unit (zillow_id, price, zestimate, house_type) values (%s, %s, %s, %s)"
    q2 = 'insert into unit_image (id, image) values ( %s, %s)'
    q3 = 'insert into unit_link (id,  link) values ( %s, %s)'
    q4 = 'insert into unit_address (id,  street, city, state, zipcode) values ( %s, %s,%s, %s, %s)'
    q5 = 'insert into unit_info (id,  beds, baths, area_sq) values ( %s, %s, %s, %s)'
    for x, house_unit in enumerate(house_units):
        cursor.execute(q1, house_unit)
        last_id = cursor.lastrowid
        cursor.execute(q2, [last_id] + unit_images[x])
        cursor.execute(q3, [last_id] + unit_links[x])
        cursor.execute(q4, [last_id] + unit_addresses[x])
        cursor.execute(q5, [last_id] + unit_infos[x])
    conn.commit()
