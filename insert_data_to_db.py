import pymysql
import zillow_config as cfg


def data_from_scraper_to_db(df):
    """Inserts data scraped from website zillow, to tables unit_house (all columns),
    address(all columns except aqi_id) in database zillow """
    # connect to mysql using pymysql
    try:
        conn = pymysql.connect(user=cfg.SQL_ROOT, password=cfg.SQL_PASS, database=cfg.DATABASE_NAME)
    except Exception as error:
        print(f'Below error occurred. Did you create the database? \n {error}')
    else:
        cursor = conn.cursor()
    # there are <0.5% data that has NaN. Fill them with 0 for easy process.
    df = df.fillna(0)
    # convert data type
    df['zpid'] = df['zpid'].astype(int)
    df['zestimate'] = df['zestimate'].astype(float)
    df['unformattedPrice'] = df['unformattedPrice'].astype(float)
    df['addressZipcode'] = df['addressZipcode'].astype(int)
    df['beds'] = df['beds'].astype(int)
    df['baths'] = df['baths'].astype(int)
    df['area'] = df['area'].astype(float)
    # select wanted columns from df and save into lists.
    unit_houses = df[['zpid', 'unformattedPrice', 'zestimate', 'statusText', 'imgSrc', 'detailUrl', 'area', 'beds','baths']].values.tolist()
    addresses = df[['addressStreet', 'addressCity', 'addressState', 'addressZipcode']].values.tolist()

    # queries for inserting data
    q0 = 'select id from unit_house where zillow_id = %s'
    q1 = "insert into unit_house (zillow_id, price, zestimate_price, house_type, image_link, unit_link, area_sq, beds, baths) values (%s, %s,%s, %s,%s, %s,%s, %s,%s) on duplicate key update price = values(price), zestimate_price = values(zestimate_price), house_type = values(house_type), image_link = values(image_link), unit_link = values(unit_link), area_sq = values(area_sq), beds = values(beds), baths = values(baths)"
    q2 = 'insert into address (id, street, city, state, zipcode) values ( %s, %s,%s, %s,%s) on duplicate key update street = values(street), city = values(city)'

    for i, house in enumerate(unit_houses):
        cursor.execute(q1, house)
        last_id = cursor.lastrowid
        if last_id != 0:
            cursor.execute(q2, [last_id] + addresses[i])
        elif last_id == 0:
            cursor.execute(q0, unit_houses[i][0])
            id_of_this_record = cursor.fetchone()
            cursor.execute(q2, [id_of_this_record] + addresses[i])
    conn.commit()


def data_from_api_school_to_db(df_school):
    """Inserts data from College Scorecard API, to tables schools (all columns),
        address_to_schools(all columns) in database zillow """
    # connect to mysql using pymysql
    try:
        conn = pymysql.connect(user=cfg.SQL_ROOT, password=cfg.SQL_PASS, database=cfg.DATABASE_NAME)
    except Exception as error:
        print(f'Below error occurred. Did you create the database? \n {error}')
    else:
        cursor = conn.cursor()

    # to insert data from df_school to table schools
    schools_s = df_school[['school_name', 'city', 'state']].values.tolist()
    q3 = 'insert into schools (school_name, city, state) values (%s, %s, %s) on duplicate key update city = values(city)'
    for school in schools_s:
        cursor.execute(q3, school)
    conn.commit()

    # to insert data from table schools(id) and table address(id) into table address_to_schools
    q5 = "select id from address"
    cursor.execute(q5)
    id_tuple_address = cursor.fetchall()
    # tb_len is table_length
    q_tb_len = 'select count(id) from address'
    cursor.execute(q_tb_len)
    tb_len = cursor.fetchone()

    for i in range(int(tb_len[0])):
        q6 = 'select city from address where id = %s'
        cursor.execute(q6, id_tuple_address[i][0])
        city_selection = cursor.fetchone()

        q7 = 'select id from schools where city = %s'
        cursor.execute(q7, city_selection)
        id_tuple_school = cursor.fetchall()

        for j in range(len(id_tuple_school)):
            q8 = 'insert into address_to_schools (address_id, school_id) values(%s, %s) on duplicate key update address_id = values(address_id), school_id = values(school_id)'
            cursor.execute(q8, [id_tuple_address[i][0], id_tuple_school[j][0]])

    conn.commit()


def data_from_api_AQI_to_db(df_aqi):
    """Inserts data from air quality index API, to tables air_quality_index (all columns),
        address(column aqi_id) in database zillow """
    # connect to mysql using pymysql
    try:
        conn = pymysql.connect(user=cfg.SQL_ROOT, password=cfg.SQL_PASS, database=cfg.DATABASE_NAME)
    except Exception as error:
        print(f'Below error occurred. Did you create the database? \n {error}')
    else:
        cursor = conn.cursor()

    # to insert data from df_school to table air_quality_index
    aqis = df_aqi[['city', 'state', 'AQI']].values.tolist()
    q9 = 'insert into air_quality_index (city, state, AQI) values (%s, %s, %s) on duplicate key update AQI = values(AQI)'
    for aqi in aqis:
        cursor.execute(q9, aqi)
    conn.commit()

    # to insert data from table air_quality_index(column id) into table address(column aqi_id)
    q_id_aqi = "select id from air_quality_index"
    cursor.execute(q_id_aqi)
    id_tuple_air_quality_index = cursor.fetchall()

    for i in range(len(id_tuple_air_quality_index)):
        q10 = 'select city, state from air_quality_index where id = %s'
        cursor.execute(q10, id_tuple_air_quality_index[i][0])
        city_state_selection = cursor.fetchone()

        q11 = 'select id from address where city = %s and state= %s'
        cursor.execute(q11, [city_state_selection[0], city_state_selection[1]])
        id_tuple_address = cursor.fetchall()

        for j in range(len(id_tuple_address)):
            q12 = 'insert into address (id, aqi_id) values(%s, %s) on duplicate key update aqi_id = values(aqi_id)'
            cursor.execute(q12, [id_tuple_address[j][0], id_tuple_air_quality_index[i][0]])
    conn.commit()
