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

    # create table house_unit
    del_existing_house_unit = 'drop table if exists house_unit'
    create_house_unit = """create table house_unit(
    id int primary key auto_increment,
    zillow_id int,
    price float not null, 
    zestimate float,
    house_type varchar(255),
    UNIQUE (zillow_id)
    )ENGINE=INNODB"""

    # create table unit_image
    del_existing_unit_image = 'drop table if exists unit_image'
    create_unit_image = """create table unit_image(
    id int primary key,
    image varchar(255),
    foreign key (id) references house_unit(id)
        on delete cascade
        on update cascade
    )ENGINE=INNODB"""

    # create table unit_address
    del_existing_unit_address = 'drop table if exists unit_address'
    create_unit_address = """create table unit_address(
    id int auto_increment primary key,
    street varchar(255),
    city varchar(255),
    state varchar(255),
    zipcode int,
    foreign key (id) references house_unit(id)
        on delete cascade
        on update cascade
    )ENGINE=INNODB"""

    # create table unit_info
    del_existing_unit_info = 'drop table if exists unit_info'
    create_unit_info = """create table unit_info(
    id int auto_increment primary key,
    beds int,
    baths int,
    area_sq float,
    foreign key (id) references house_unit(id)
        on delete cascade
        on update cascade 
    )ENGINE=INNODB"""

    # create table unit_link
    del_existing_unit_link = 'drop table if exists unit_link'
    create_unit_link = """create table unit_link(
    id int primary key,
    link varchar(255),
    foreign key (id) references house_unit(id)
        on delete cascade
        on update cascade 
    )ENGINE=INNODB"""

    cursor.execute(del_existing_house_unit)
    cursor.execute(create_house_unit)
    print('table house_unit is created.')

    cursor.execute(del_existing_unit_image)
    cursor.execute(create_unit_image)
    print('table unit_image is created.')

    cursor.execute(del_existing_unit_address)
    cursor.execute(create_unit_address)
    print('table unit_address is created.')

    cursor.execute(del_existing_unit_info)
    cursor.execute(create_unit_info)
    print('table unit_type is created.')

    cursor.execute(del_existing_unit_link)
    cursor.execute(create_unit_link)
    print('table unit_link is created.')


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
