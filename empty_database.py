"""Below code creates empty database zillow, and tables inside. """
import pymysql
import zillow_config as cfg


def get_connection():
    """Create a connection to MySQL. Need to insert specific user and password to run."""
    conn = pymysql.connect(user=cfg.SQL_ROOT, password=cfg.SQL_PASS)
    return conn


def get_cursor(conn):
    """Create a cursor to the connection."""
    cursor = conn.cursor()
    return cursor


def create_db(cursor):
    """Create a database called zillow. """
    del_existing_db = 'drop database if exists zillow'
    create_db_zillow = 'create database zillow'
    cursor.execute(del_existing_db)
    cursor.execute(create_db_zillow)
    print('db zillow is created.')


def create_tables(cursor):
    """Creates tables inside database zillow. """
    cursor.execute('use zillow')

    # create table unit_house
    del_existing_unit_house = 'drop table if exists unit_house'
    create_unit_house = """create table unit_house(
    id int primary key auto_increment,
    zillow_id int,
    price float not null, 
    zestimate float,
    house_type varchar(255),
    image_link varchar(255),
    unit_link varchar(255),
    area_sq float,
    beds int, 
    baths int,
    UNIQUE (zillow_id)
    )ENGINE=INNODB"""

    # create table air_quality_index
    del_existing_air_quality_index = 'drop table if exists air_quality_index'
    create_air_quality_index = """create table air_quality_index(
    id int primary key auto_increment,
    city varchar(255),
    AQI int,
    UNIQUE (city)
    )ENGINE=INNODB"""

    # create table address
    del_existing_address = 'drop table if exists address'
    create_address = """create table address(
    id int primary key,
    street varchar(255),
    city varchar(255),
    zipcode int,
    foreign key (id) references unit_house(id), 
    foreign key (city) references air_quality_index(city) 
        on delete cascade
        on update cascade
    )ENGINE=INNODB"""

    # create table schools
    del_existing_schools = 'drop table if exists schools'
    create_schools = """create table schools(
      id int auto_increment primary key,
      school_name varchar(255),
      city varchar(255)
      )ENGINE=INNODB"""

    # create table address_to_schools
    del_existing_address_to_schools = 'drop table if exists address_to_schools'
    create_address_to_schools = """create table address_to_schools(
    address_id int, 
    school_id int,
    foreign key (address_id) references address(id),
    foreign key (school_id) references schools(id)
        on delete cascade
        on update cascade
    )ENGINE=INNODB"""

    cursor.execute(del_existing_unit_house)
    cursor.execute(create_unit_house)
    print('table unit_house is created.')

    cursor.execute(del_existing_air_quality_index)
    cursor.execute(create_air_quality_index)
    print('table air_quality_index is created.')

    cursor.execute(del_existing_address)
    cursor.execute(create_address)
    print('table address is created.')

    cursor.execute(del_existing_schools)
    cursor.execute(create_schools)
    print('table schools is created.')

    cursor.execute(del_existing_address_to_schools)
    cursor.execute(create_address_to_schools)
    print('table address_to_schools is created.')


def main():
    """ Starting function of the program, calls above functions to create an empty database """
    sql_connection = get_connection()
    cursor = get_cursor(sql_connection)
    create_db(cursor)
    create_tables(cursor)
    sql_connection.commit()
    sql_connection.close()


if __name__ == '__main__':
    main()
