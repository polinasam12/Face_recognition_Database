import time
from tkinter import *
from tkinter import ttk
import cv2
import face_recognition
import os
from PIL import Image, ImageTk
import shutil
import pickle
import sys
import speech_recognition
import psycopg2
from config import host, user, password, db_name
import re


def create_table_images():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists IMAGES (
                    ImageId serial PRIMARY KEY,
                    FaceEncoding BYTEA NOT NULL,
                    IdentifiedPersonId integer NULL,
                    CONSTRAINT fk_image_identified_person FOREIGN KEY (IdentifiedPersonId) REFERENCES IDENTIFIED_PERSONS (IdentifiedPersonId) ON DELETE CASCADE,
                    UnidentifiedPersonId integer NULL,
                    CONSTRAINT fk_image_unidentified_person FOREIGN KEY (UnidentifiedPersonId) REFERENCES UNIDENTIFIED_PERSONS (UnidentifiedPersonId) ON DELETE CASCADE,
                    DateAndTime TIMESTAMP NOT NULL,
                    CONSTRAINT check_ids CHECK ((IdentifiedPersonId IS NOT NULL AND UnidentifiedPersonId IS NULL) or (IdentifiedPersonId IS NULL AND UnidentifiedPersonId IS NOT NULL))
                    );"""
            )
            print("CREATE TABLE if not exists IMAGES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def create_table_identified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists IDENTIFIED_PERSONS(
                    IdentifiedPersonId serial PRIMARY KEY,
                    Name varchar(50) UNIQUE NOT NULL,
                    DateAndTimeOfFirstRecognition TIMESTAMP NOT NULL,
                    DateAndTimeOfLastRecognition TIMESTAMP NOT NULL
                    );"""
            )
            print("CREATE TABLE if not exists IDENTIFIED_PERSONS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def create_table_unidentified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists UNIDENTIFIED_PERSONS(
                    UnidentifiedPersonId serial PRIMARY KEY,
                    DateAndTimeOfFirstRecognition TIMESTAMP NOT NULL,
                    DateAndTimeOfLastRecognition TIMESTAMP NOT NULL
                    );"""
            )
            print("CREATE TABLE if not exists UNIDENTIFIED_PERSONS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def create_table_access_data():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists ACCESS_DATA(
                    AccessDataId serial PRIMARY KEY,
                    Name varchar(50) UNIQUE NOT NULL,
                    Email varchar(50) UNIQUE NOT NULL,
                    Password text NOT NULL,
                    IdentifiedPersonId integer NULL,
                    CONSTRAINT fk_access_data_identified_persons FOREIGN KEY (IdentifiedPersonId) REFERENCES IDENTIFIED_PERSONS (IdentifiedPersonId) ON DELETE SET NULL
                    );"""
            )
            print("CREATE TABLE if not exists ACCESS_DATA")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def create_table_total_system_statistics():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists TOTAL_SYSTEM_STATISTICS(
                    TotalSystemStatisticsId serial PRIMARY KEY,
                    DateAndTime TIMESTAMP NOT NULL,
                    NumberOfImages integer NOT NULL,
                    NumberOfIdentifiedPersons integer NOT NULL,
                    NumberOfUnidentifiedPersons integer NOT NULL,
                    TypeOfChangeId INTEGER NOT NULL,
                    CONSTRAINT fk_total_system_statistics_type_of_changes FOREIGN KEY (TypeOfChangeId) REFERENCES TYPES_OF_CHANGES (TypeOfChangeId) ON DELETE NO ACTION
                    );"""
            )
            print("CREATE TABLE if not exists TOTAL_SYSTEM_STATISTICS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def create_table_types_of_changes():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE if not exists TYPES_OF_CHANGES(
                    TypeOfChangeId serial PRIMARY KEY,
                    Description varchar(150) UNIQUE NOT NULL
                    );"""
            )
            print("CREATE TABLE if not exists TYPES_OF_CHANGES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_images():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE IMAGES;"""
            )
            print("DROP TABLE IMAGES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_identified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE IDENTIFIED_PERSONS;"""
            )
            print("DROP TABLE IDENTIFIED_PERSONS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_unidentified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE UNIDENTIFIED_PERSONS;"""
            )
            print("DROP TABLE UNIDENTIFIED_PERSONS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_access_data():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE ACCESS_DATA;"""
            )
            print("DROP TABLE ACCESS_DATA")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_total_system_statistics():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE TOTAL_SYSTEM_STATISTICS;"""
            )
            print("DROP TABLE TOTAL_SYSTEM_STATISTICS")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def drop_table_types_of_changes():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE TYPES_OF_CHANGES;"""
            )
            print("DROP TABLE TYPES_OF_CHANGES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_identified_person_image_into_images(face_encoding, identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO IMAGES(FaceEncoding, IdentifiedPersonId, DateAndTime) VALUES (%s, %s, NOW());""",
                (face_encoding, identified_person_id)
            )
            print("INSERT INTO IMAGES(FaceEncoding, IdentifiedPersonId)")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_unidentified_person_image_into_images(face_encoding, unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO IMAGES(FaceEncoding, UnidentifiedPersonId, DateAndTime) VALUES (%s, %s, NOW());""", (face_encoding, unidentified_person_id))
            print("INSERT INTO IMAGES(FaceEncoding, UnidentifiedPersonId)")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_identified_persons(name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO IDENTIFIED_PERSONS(Name, DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES ('" + name + "', NOW(), NOW());")
            print("INSERT INTO IDENTIFIED_PERSONS(Name, DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_identified_persons_with_date_and_time_of_first_and_last_recognitions(name, date_and_time_of_first_recognition, date_and_time_of_last_recognition):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO IDENTIFIED_PERSONS(Name, DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES ('" + name + "', '" + str(date_and_time_of_first_recognition) + "', '" + str(date_and_time_of_last_recognition) + "');")
            print("INSERT INTO IDENTIFIED_PERSONS(Name, DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_unidentified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO UNIDENTIFIED_PERSONS(DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES (NOW(), NOW());")
            print("INSERT INTO UNIDENTIFIED_PERSONS(DateAndTimeOfFirstRecognition, DateAndTimeOfLastRecognition) VALUES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_access_data(name, email, passw):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE EXTENSION IF NOT EXISTS pgcrypto;
                INSERT INTO ACCESS_DATA(Name, Email, Password) VALUES (%s, %s, crypt(%s, gen_salt('md5')));
                """, (name, email, passw))
            print("INSERT INTO ACCESS_DATA(Name, Email, Password) VALUES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_access_data_with_fk(name, email, passw, identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE EXTENSION IF NOT EXISTS pgcrypto;
                INSERT INTO ACCESS_DATA(Name, Email, Password, IdentifiedPersonId) VALUES (%s, %s, crypt(%s, gen_salt('md5')), %s);
                """, (name, email, passw, identified_person_id))
            print("INSERT INTO ACCESS_DATA(Name, Email, Password, IdentifiedPersonId)")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_types_of_changes(description):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO TYPES_OF_CHANGES(Description) VALUES ('" + description + "');")
            print("INSERT INTO TYPES_OF_CHANGES(Description) VALUES")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def insert_into_total_system_statistics(number_of_images, number_of_identified_persons, number_of_unidentified_persons, type_of_change_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO TOTAL_SYSTEM_STATISTICS(DateAndTime, NumberOfImages, NumberOfIdentifiedPersons, NumberOfUnidentifiedPersons, TypeOfChangeId) VALUES (NOW(), %s, %s, %s, %s);
                """, (number_of_images, number_of_identified_persons, number_of_unidentified_persons, type_of_change_id))
            print("INSERT INTO TOTAL_SYSTEM_STATISTICS(DateAndTime, NumberOfImages, NumberOfIdentifiedPersons, NumberOfUnidentifiedPersons, TypeOfChangeId)")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_images():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM IMAGES;")
            print("SELECT COUNT(*) FROM IMAGES")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_identified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM IDENTIFIED_PERSONS;")
            print("SELECT COUNT(*) FROM IDENTIFIED_PERSONS")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_types_of_changes():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM TYPES_OF_CHANGES;")
            print("SELECT COUNT(*) FROM TYPES_OF_CHANGES")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_unidentified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM UNIDENTIFIED_PERSONS;")
            print("SELECT COUNT(*) FROM UNIDENTIFIED_PERSONS")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_images_of_identified_person(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM IMAGES WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("SELECT COUNT(*) FROM IMAGES WHERE IdentifiedPersonId =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def count_images_of_unidentified_person(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM IMAGES WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("SELECT COUNT(*) FROM IMAGES WHERE UnidentifiedPersonId =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_id_by_name_in_table_identified_persons(name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("SELECT IdentifiedPersonId FROM IDENTIFIED_PERSONS WHERE Name = '" + name + "';")
            print("SELECT IdentifiedPersonId FROM IDENTIFIED_PERSONS WHERE Name =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_access_data_with_fk(name, identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("UPDATE ACCESS_DATA SET IdentifiedPersonId = %s WHERE Name = %s;", (identified_person_id, name))
            print("UPDATE ACCESS_DATA SET IdentifiedPersonId = %s WHERE Name = %s;")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_name_by_id_in_table_identified_persons(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT Name FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("SELECT Name FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def find_identified_person_face_encoding_in_table_images(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT FaceEncoding FROM IMAGES WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("SELECT FaceEncoding FROM IMAGES WHERE IdentifiedPersonId =")
            return pickle.loads(cursor.fetchone()[0])
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def find_unidentified_person_face_encoding_in_table_images(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT FaceEncoding FROM IMAGES WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("SELECT FaceEncoding FROM IMAGES WHERE UnidentifiedPersonId = ")
            return pickle.loads(cursor.fetchone()[0])
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def is_there_this_email_in_table_access_data(email):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM ACCESS_DATA WHERE Email = '" + email + "');")
            print("SELECT EXISTS (SELECT 1 FROM ACCESS_DATA WHERE Email =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def is_there_this_name_in_table_access_data(name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM ACCESS_DATA WHERE Name = '" + name + "');")
            print("SELECT EXISTS (SELECT 1 FROM ACCESS_DATA WHERE Name =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def is_there_this_name_in_table_identified_persons(name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM IDENTIFIED_PERSONS WHERE Name = '" + name + "');")
            print("SELECT EXISTS (SELECT 1 FROM IDENTIFIED_PERSONS WHERE Name =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def is_there_this_id_in_table_unidentified_persons(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ");")
            print("SELECT EXISTS (SELECT 1 FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId =")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def is_this_person_recognized_in_time_interval(identified_person_id, start_time, end_time):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (SELECT 1 FROM IMAGES WHERE IdentifiedPersonId = %s AND %s <= DateAndTime AND DateAndTime <= %s);
                """,
                (identified_person_id, start_time, end_time)
            )
            print("SELECT EXISTS (SELECT 1 FROM IMAGES WHERE IdentifiedPersonId = ")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_statistics_list_from_time_interval(start_time, end_time):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DateAndTime, NumberOfImages, NumberOfIdentifiedPersons, NumberOfUnidentifiedPersons, TypeOfChangeId FROM TOTAL_SYSTEM_STATISTICS WHERE %s <= DateAndTime AND DateAndTime <= %s;
                """,
                (start_time, end_time)
            )
            print("SELECT DateAndTime, NumberOfImages, NumberOfIdentifiedPersons, NumberOfUnidentifiedPersons, TypeOfChangeId FROM TOTAL_SYSTEM_STATISTICS WHERE")
            return cursor.fetchall()
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def delete_from_table_unidentified_persons_by_id(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("DELETE FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId =")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_date_and_time_of_first_recognition_in_table_unidentified_persons(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT DateAndTimeOfFirstRecognition FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("SELECT DateAndTimeOfFirstRecognition FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = ")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_date_and_time_of_last_recognition_in_table_unidentified_persons(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT DateAndTimeOfLastRecognition FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("SELECT DateAndTimeOfLastRecognition FROM UNIDENTIFIED_PERSONS WHERE UnidentifiedPersonId = ")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_date_and_time_of_first_recognition_in_table_identified_persons(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT DateAndTimeOfFirstRecognition FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("SELECT DateAndTimeOfFirstRecognition FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId = ")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_date_and_time_of_last_recognition_in_table_identified_persons(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT DateAndTimeOfLastRecognition FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("SELECT DateAndTimeOfLastRecognition FROM IDENTIFIED_PERSONS WHERE IdentifiedPersonId = ")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_unidentified_person_id_to_identified_person_id_in_table_images(unidentified_person_id, identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("UPDATE IMAGES SET IdentifiedPersonId = " + str(identified_person_id) + ", UnidentifiedPersonId = NULL WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("UPDATE IMAGES SET IdentifiedPersonId = ")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def check_email_and_password_in_table_access_data(email, passw):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE EXTENSION IF NOT EXISTS pgcrypto;
                SELECT Password = crypt(%s, Password) FROM ACCESS_DATA WHERE Email = %s;
                """, (passw, email)
            )
            print("SELECT Password = crypt(%s, Password) FROM ACCESS_DATA WHERE Email = %s")
            return cursor.fetchone()[0]
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_name_in_identified_persons(old_name, new_name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("UPDATE IDENTIFIED_PERSONS SET Name = '" + new_name + "' WHERE Name = '" + old_name + "';")
            print("UPDATE IDENTIFIED_PERSONS SET Name =")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_name_in_access_data(old_name, new_name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("UPDATE ACCESS_DATA SET Name = '" + new_name + "' WHERE Name = '" + old_name + "';")
            print("UPDATE ACCESS_DATA SET Name =")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_date_and_time_of_last_recognition_in_table_identified_persons(identified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("UPDATE IDENTIFIED_PERSONS SET DateAndTimeOfLastRecognition = NOW() WHERE IdentifiedPersonId = " + str(identified_person_id) + ";")
            print("UPDATE IDENTIFIED_PERSONS SET DateAndTimeOfLastRecognition = NOW() WHERE IdentifiedPersonId = ")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def update_date_and_time_of_last_recognition_in_table_unidentified_persons(unidentified_person_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("UPDATE UNIDENTIFIED_PERSONS SET DateAndTimeOfLastRecognition = NOW() WHERE UnidentifiedPersonId = " + str(unidentified_person_id) + ";")
            print("UPDATE UNIDENTIFIED_PERSONS SET DateAndTimeOfLastRecognition = NOW() WHERE UnidentifiedPersonId =")
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_ids_from_table_identified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT IdentifiedPersonId FROM IDENTIFIED_PERSONS;")
            print("SELECT IdentifiedPersonId FROM IDENTIFIED_PERSONS")
            return cursor.fetchall()
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def get_ids_from_table_unidentified_persons():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("SELECT UnidentifiedPersonId FROM UNIDENTIFIED_PERSONS;")
            print("SELECT UnidentifiedPersonId FROM UNIDENTIFIED_PERSONS")
            return cursor.fetchall()
    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            connection.close()


def listen():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return None


def delete_dataset():
    folders = os.listdir("dataset")
    for folder in folders:
        shutil.rmtree("dataset/" + folder)

    drop_table_images()
    drop_table_access_data()
    drop_table_identified_persons()
    drop_table_unidentified_persons()
    drop_table_total_system_statistics()
    drop_table_types_of_changes()

    create_table_identified_persons()
    create_table_unidentified_persons()
    create_table_images()
    create_table_access_data()
    create_table_types_of_changes()
    insert_types_of_changes()
    create_table_total_system_statistics()


def is_name_belongs_to_unidentified_person(name):
    return name[:6] == "person" and name[6:].isdigit() and is_there_this_id_in_table_unidentified_persons(int(name[6:]))
    
    
def is_name_belongs_to_identified_person(name):
    return is_there_this_name_in_table_identified_persons(name)


def change_name(old_name, new_name):
    if is_name_belongs_to_identified_person(old_name) and not(is_name_belongs_to_identified_person(new_name)) and not(is_name_belongs_to_unidentified_person(new_name)) and new_name != "":
        update_name_in_identified_persons(old_name, new_name)
        if is_there_this_name_in_table_access_data(old_name):
            update_name_in_access_data(old_name, new_name)
        dialog_label.config(text="Имя " + old_name + " изменено на " + new_name, width="50")
        dialog_label.update_idletasks()
        if os.path.isdir("dataset/" + old_name):
            os.rename("dataset/" + old_name, "dataset/" + new_name)
    elif is_name_belongs_to_unidentified_person(old_name) and not(is_name_belongs_to_identified_person(new_name)) and not(is_name_belongs_to_unidentified_person(new_name)) and new_name != "":
        unidentified_person_id = int(old_name[6:])
        date_and_time_of_first_recognition = get_date_and_time_of_first_recognition_in_table_unidentified_persons(unidentified_person_id)
        date_and_time_of_last_recognition = get_date_and_time_of_last_recognition_in_table_unidentified_persons(unidentified_person_id)
        insert_into_identified_persons_with_date_and_time_of_first_and_last_recognitions(new_name, date_and_time_of_first_recognition, date_and_time_of_last_recognition)
        identified_person_id = count_identified_persons()
        if is_there_this_name_in_table_access_data(new_name):
            update_access_data_with_fk(new_name, identified_person_id)
        update_unidentified_person_id_to_identified_person_id_in_table_images(unidentified_person_id, identified_person_id)
        delete_from_table_unidentified_persons_by_id(unidentified_person_id)
        dialog_label.config(text="Имя " + old_name + " изменено на " + new_name, width="50")
        dialog_label.update_idletasks()
        if os.path.isdir("dataset/" + old_name):
            os.rename("dataset/" + old_name, "dataset/" + new_name)
    else:
        dialog_label.config(text="Имена введены некорректно", width="50")
        dialog_label.update_idletasks()


def change_name_from_speech_recognition():
    global name_now, number_of_persons_in_front_of_the_camera
    if number_of_persons_in_front_of_the_camera == 0:
        dialog_label.config(text='Перед камерой никого нет', width="50")
        dialog_label.update_idletasks()
        return
    if number_of_persons_in_front_of_the_camera > 1:
        dialog_label.config(text='Перед камерой находится более одного человека', width="50")
        dialog_label.update_idletasks()
        return
    dialog_label.config(text='Скажите имя', width="50")
    dialog_label.update_idletasks()
    query = listen()
    if query:
        change_name(name_now, query[0].upper() + query[1:])
        insert_statistic(4)
    else:
        dialog_label.config(text='Не получилось распознать имя', width="50")
        dialog_label.update_idletasks()


def change_name_from_input_person_name_in_front_of_camera():
    global input_person_name_in_front_of_camera, dialog_label, number_of_persons_in_front_of_the_camera
    if number_of_persons_in_front_of_the_camera == 0:
        dialog_label.config(text='Перед камерой никого нет', width="50")
        dialog_label.update_idletasks()
        return
    if number_of_persons_in_front_of_the_camera > 1:
        dialog_label.config(text='Перед камерой находится более одного человека', width="50")
        dialog_label.update_idletasks()
        return
    old_name = name_now
    new_name = input_person_name_in_front_of_camera.get()
    change_name(old_name, new_name)
    insert_statistic(3)


def change_name_from_input_now_name_and_input_new_name():
    global input_now_name, input_new_name
    old_name = input_now_name.get()
    new_name = input_new_name.get()
    change_name(old_name, new_name)
    insert_statistic(2)


def insert_types_of_changes():
    if count_types_of_changes() == 0:
        insert_into_types_of_changes("Распознан новый человек")
        insert_into_types_of_changes("Изменено имя вводом текущего имени и нового имени текстом")
        insert_into_types_of_changes("Изменено имя вводом имени человека, находящегося перед камерой, текстом")
        insert_into_types_of_changes("Изменено имя прослушиванием имени человека, находящегося перед камерой")


def insert_statistic(type_of_change_id):
    number_of_images = count_images()
    number_of_identified_persons = count_identified_persons()
    number_of_unidentified_persons = count_unidentified_persons()
    insert_into_total_system_statistics(number_of_images, number_of_identified_persons, number_of_unidentified_persons, type_of_change_id)


def start():
    global last_time, new_time, name_now, number_of_persons_in_front_of_the_camera
    success, image = cap.read()
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image, locations)
    is_3_sec_passed = False
    number_of_persons_in_front_of_the_camera = len(locations)
    for face_location, face_encoding in zip(locations, encodings):
        name = ""
        recognized_identified_person_id = 0
        recognized_unidentified_person_id = 0
        identified_person_ids = get_ids_from_table_identified_persons()
        unidentified_person_ids = get_ids_from_table_unidentified_persons()
        if identified_person_ids:
            identified_person_number = len(identified_person_ids)
        else:
            identified_person_number = 0
        if unidentified_person_ids:
            unidentified_person_number = len(unidentified_person_ids)
        else:
            unidentified_person_number = 0
        for i in range(identified_person_number):
            identified_person_id = identified_person_ids[i][0]
            identified_person_face_encoding = find_identified_person_face_encoding_in_table_images(identified_person_id)
            if face_recognition.compare_faces([face_encoding], identified_person_face_encoding)[0]:
                recognized_identified_person_id = identified_person_id
                name = get_name_by_id_in_table_identified_persons(identified_person_id)
                break
        for i in range(unidentified_person_number):
            unidentified_person_id = unidentified_person_ids[i][0]
            unidentified_person_face_encoding = find_unidentified_person_face_encoding_in_table_images(unidentified_person_id)
            if face_recognition.compare_faces([face_encoding], unidentified_person_face_encoding)[0]:
                recognized_unidentified_person_id = unidentified_person_id
                name = "person" + str(recognized_unidentified_person_id)
                break
        top, right, bottom, left = face_location
        left_top = (left, top)
        right_bottom = (right, bottom)
        color = [255, 0, 0]
        cv2.rectangle(image, left_top, right_bottom, color, 4)
        new_time = time.time()
        if new_time - last_time >= 3:
            is_3_sec_passed = True
            face_img = image[top:bottom, left:right]
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(face_img)
            if recognized_identified_person_id != 0:
                count = count_images_of_identified_person(recognized_identified_person_id) + 1
                pil_img.save("dataset/" + name + "/" f"img_{count}.jpg")
                insert_identified_person_image_into_images(pickle.dumps(face_encoding), recognized_identified_person_id)
                update_date_and_time_of_last_recognition_in_table_identified_persons(recognized_identified_person_id)
            elif recognized_unidentified_person_id != 0:
                count = count_images_of_unidentified_person(recognized_unidentified_person_id) + 1
                pil_img.save("dataset/" + name + "/" f"img_{count}.jpg")
                insert_unidentified_person_image_into_images(pickle.dumps(face_encoding), recognized_unidentified_person_id)
                update_date_and_time_of_last_recognition_in_table_unidentified_persons(recognized_unidentified_person_id)
            else:
                count = identified_person_number + unidentified_person_number + 1
                name = f"person{count}"
                os.makedirs("dataset/" + name)
                pil_img.save("dataset/" + name + "/" + f"img_1.jpg")
                insert_into_unidentified_persons()
                insert_unidentified_person_image_into_images(pickle.dumps(face_encoding), count)
                insert_statistic(1)
        left_bottom = (left, bottom)
        right_bottom = (right, bottom + 20)
        name_now = name
        cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
        cv2.putText(image, name, (left + 10, bottom + 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4)
    if is_3_sec_passed:
        last_time = new_time
    frame = image
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    main_label.imgtk = imgtk
    main_label.configure(image=imgtk)
    main_label.after(10, start)


def close_program():
    sys.exit()


def recognized_persons_in_time_interval():
    global input_start_date_and_time, input_final_date_and_time, label_persons_list
    start_date_and_time = input_start_date_and_time.get()
    final_date_and_time = input_final_date_and_time.get()
    if not(is_date_and_time_correct(start_date_and_time)) or not(is_date_and_time_correct(final_date_and_time)):
        label_persons_list.config(text="Дата и время введены некорректно", width="50")
        label_persons_list.update_idletasks()
        return
    if is_only_date(start_date_and_time):
        start_date_and_time += " 00:00:00"
    if is_only_date(final_date_and_time):
        final_date_and_time += " 23:59:59"
    identified_person_ids = get_ids_from_table_identified_persons()
    if identified_person_ids:
        identified_person_number = len(identified_person_ids)
    else:
        identified_person_number = 0
    persons = []
    for i in range(identified_person_number):
        identified_person_id = identified_person_ids[i][0]
        if is_this_person_recognized_in_time_interval(identified_person_id, start_date_and_time, final_date_and_time):
            name = get_name_by_id_in_table_identified_persons(identified_person_id)
            persons.append(name)
    persons_str = ", ".join(persons)
    label_persons_list.config(text=persons_str, width="50")
    label_persons_list.update_idletasks()


def statistics():
    global input_start_date_and_time, input_final_date_and_time, label_persons_list
    global tree
    start_date_and_time = input_start_date_and_time.get()
    final_date_and_time = input_final_date_and_time.get()
    if not (is_date_and_time_correct(start_date_and_time)) or not (is_date_and_time_correct(final_date_and_time)):
        label_persons_list.config(text="Дата и время введены некорректно", width="50")
        label_persons_list.update_idletasks()
        return
    if is_only_date(start_date_and_time):
        start_date_and_time += " 00:00:00"
    if is_only_date(final_date_and_time):
        final_date_and_time += " 23:59:59"
    statistics_list = get_statistics_list_from_time_interval(start_date_and_time, final_date_and_time)
    tree.delete(*tree.get_children())
    tree.heading("1", text="Дата и время")
    tree.heading("2", text="Число изображений")
    tree.heading("3", text="Число идентифицированных людей")
    tree.heading("4", text="Число неидентифицированных людей")
    tree.heading("5", text="Тип изменения")
    for statistic in statistics_list:
        tree.insert("", END, values=statistic)


def person_information():
    global input_person_info, label_person_info
    name = input_person_info.get()
    identified_person_id = get_id_by_name_in_table_identified_persons(name)
    date_and_time_of_first_recognition = get_date_and_time_of_first_recognition_in_table_identified_persons(identified_person_id)
    date_and_time_of_last_recognition = get_date_and_time_of_last_recognition_in_table_identified_persons(identified_person_id)
    person_info = "Дата и время первого распознавания: " + str(date_and_time_of_first_recognition) + "\nДата и время последнего распознавания: " + str(date_and_time_of_last_recognition) + "\n"
    label_person_info.config(text=person_info, width="100")
    label_person_info.update_idletasks()


def is_email_correct(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def is_date_and_time_correct(date_and_time):
    regex = re.compile(r'\d{4}-\d{2}-\d{2}(\s\d{2}:\d{2}:\d{2})?')
    if re.fullmatch(regex, date_and_time):
        return True
    else:
        return False


def is_only_date(date):
    regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    if re.fullmatch(regex, date):
        return True
    else:
        return False


def register():
    global input_name_reg, input_email_reg, input_pass1_reg, input_pass2_reg, label_reg
    name_reg = input_name_reg.get()
    email_reg = input_email_reg.get()
    pass1_reg = input_pass1_reg.get()
    pass2_reg = input_pass2_reg.get()
    if len(name_reg) == 0:
        label_reg.config(text='Имя не введено\n', width="50")
        return
    if len(email_reg) == 0:
        label_reg.config(text='Адрес электронной почты не введён\n', width="50")
        return
    if not (is_email_correct(email_reg)):
        label_reg.config(text='Адрес электронной почты введён некорректно\n', width="50")
        return
    if len(pass1_reg) < 6:
        label_reg.config(text='Длина пароля должна быть не менее 6 символов\n', width="50")
        return
    if pass1_reg != pass2_reg:
        label_reg.config(text='Пароли не совпадают\n', width="50")
        return
    same_email = is_there_this_email_in_table_access_data(email_reg)
    same_name = is_there_this_name_in_table_access_data(name_reg)
    if same_email:
        label_reg.config(text='Такой адрес электронной почты уже существует\n', width="50")
        return
    if same_name:
        label_reg.config(text='Такое имя уже существует\n', width="50")
        return
    is_exist_name_reg_in_persons = is_there_this_name_in_table_identified_persons(name_reg)
    if is_exist_name_reg_in_persons:
        person_id = get_id_by_name_in_table_identified_persons(name_reg)
        insert_into_access_data_with_fk(name_reg, email_reg, pass1_reg, person_id)
        label_reg.config(text='Регистрация прошла успешно!\n', width="50")
    else:
        insert_into_access_data(name_reg, email_reg, pass1_reg)
        label_reg.config(text='Регистрация прошла успешно!\n', width="50")


def enter_recognition_window():
    global input_authorize_email, input_authorize_pass, label_authorize
    email_authorize = input_authorize_email.get()
    pass_authorize = input_authorize_pass.get()
    if not(is_there_this_email_in_table_access_data(email_authorize)):
        label_authorize.config(text='Введен неверный адрес электронной почты или пароль\n', width="50")
        return
    check_password = check_email_and_password_in_table_access_data(email_authorize, pass_authorize)
    if check_password:
        window.destroy()
        create_recognition_window()
    else:
        label_authorize.config(text='Введен неверный адрес электронной почты или пароль\n', width="50")


def enter_output_window():
    global input_authorize_email, input_authorize_pass, label_authorize
    email_authorize = input_authorize_email.get()
    pass_authorize = input_authorize_pass.get()
    if not(is_there_this_email_in_table_access_data(email_authorize)):
        label_authorize.config(text='Введен неверный адрес электронной почты или пароль\n', width="50")
        return
    check_password = check_email_and_password_in_table_access_data(email_authorize, pass_authorize)
    if check_password:
        window.destroy()
        create_output_window()
    else:
        label_authorize.config(text='Введен неверный адрес электронной почты или пароль\n', width="50")


def create_authorization_window():
    global window, input_name_reg, input_email_reg, input_pass1_reg, input_pass2_reg, label_reg, input_authorize_email, input_authorize_pass, label_authorize

    window = Tk()
    window.wm_title("Face recognition system with database")
    window.config(background="#FFFFFF")

    command_frame = Frame(window, width=600, height=500)
    command_frame.grid(row=800, column=0, padx=10, pady=2)

    title1 = Label(command_frame, text="Регистрация", font=('Helvetica', 14, 'bold'))
    title1.pack()
    title2 = Label(command_frame, text="Введите имя", bg="white", font=40)
    title2.pack()
    input_name_reg = Entry(command_frame, bg="white")
    input_name_reg.pack()
    title3 = Label(command_frame, text="Введите адрес электронной почты", bg="white", font=40)
    title3.pack()
    input_email_reg = Entry(command_frame, bg="white")
    input_email_reg.pack()
    title4 = Label(command_frame, text="Введите пароль", bg="white", font=40)
    title4.pack()
    input_pass1_reg = Entry(command_frame, show="*", bg="white")
    input_pass1_reg.pack()
    title5 = Label(command_frame, text="Повторите пароль", bg="white", font=40)
    title5.pack()
    input_pass2_reg = Entry(command_frame, show="*", bg="white")
    input_pass2_reg.pack()
    btn1 = Button(command_frame, text="Зарегистрироваться", bg="white", font=40, command=register)
    btn1.pack()
    label_reg = Label(command_frame, font=40)
    label_reg.pack()

    title6 = Label(command_frame, text="Вход", font=('Helvetica', 14, 'bold'))
    title6.pack()
    title7 = Label(command_frame, text="Введите адрес электронной почты", bg="white", font=40)
    title7.pack()
    input_authorize_email = Entry(command_frame, bg="white")
    input_authorize_email.pack()
    title8 = Label(command_frame, text="Введите пароль", bg="white", font=40)
    title8.pack()
    input_authorize_pass = Entry(command_frame, show="*", bg="white")
    input_authorize_pass.pack()
    btn2 = Button(command_frame, text="Войти в систему распознавания лиц и ввода имен", bg="white", font=40, command=enter_recognition_window)
    btn2.pack()
    btn3 = Button(command_frame, text="Войти в систему вывода информации", bg="white", font=40, command=enter_output_window)
    btn3.pack()
    label_authorize = Label(command_frame, font=40)
    label_authorize.pack()
    btn4 = Button(command_frame, text="Очистить базу данных", bg="white", font=40, command=delete_dataset)
    btn4.pack()
    btn5 = Button(command_frame, text="Выйти", bg="white", font=40, command=close_program)
    btn5.pack()
    window.mainloop()


def create_recognition_window():
    global window, main_label, dialog_label, cap
    global input_person_name_in_front_of_camera, input_now_name, input_new_name
    window = Tk()
    window.wm_title("Face recognition system with database")
    window.config(background="#FFFFFF")

    image_frame = Frame(window, width=600, height=500)
    image_frame.grid(row=0, column=0, padx=10, pady=2)

    main_label = Label(image_frame, width=580, height=496)
    main_label.grid(row=0, column=0)
    cap = cv2.VideoCapture(0)

    dialog_frame = Frame(window, width=600, height=300)
    dialog_frame.grid(row=500, column=0, padx=10, pady=2)

    dialog_label = Label(dialog_frame, text="", width=70)
    dialog_label.pack()

    command_frame = Frame(window, width=600, height=500)
    command_frame.grid(row=800, column=0, padx=10, pady=2)

    title1 = Label(command_frame, text="Голосовой ввод имени человека, находящегося перед камерой", font=('Helvetica', 14, 'bold'))
    title1.pack()
    btn1 = Button(command_frame, text="Прослушать имя", bg="white", font=40, command=change_name_from_speech_recognition)
    btn1.pack()
    title_empty1 = Label(command_frame)
    title_empty1.pack()

    title2 = Label(command_frame, text="Текстовый ввод имени человека, находящегося перед камерой", font=('Helvetica', 14, 'bold'))
    title2.pack()
    input_person_name_in_front_of_camera = Entry(command_frame, bg="white")
    input_person_name_in_front_of_camera.pack()
    btn2 = Button(command_frame, text="Ввести имя", bg="white", font=40, command=change_name_from_input_person_name_in_front_of_camera)
    btn2.pack()
    title_empty2 = Label(command_frame)
    title_empty2.pack()

    title3 = Label(command_frame, text="Изменение имени", font=('Helvetica', 14, 'bold'))
    title3.pack()
    title4 = Label(command_frame, text="Текущее имя", bg="white", font=40)
    title4.pack()
    input_now_name = Entry(command_frame, bg="white")
    input_now_name.pack()
    title5 = Label(command_frame, text="Новое имя", bg="white", font=40)
    title5.pack()
    input_new_name = Entry(command_frame, bg="white")
    input_new_name.pack()
    btn3 = Button(command_frame, text="Изменить имя", bg="white", font=40, command=change_name_from_input_now_name_and_input_new_name)
    btn3.pack()
    title_empty3 = Label(command_frame)
    title_empty3.pack()

    btn4 = Button(command_frame, text="Очистить базу данных", bg="white", font=40, command=delete_dataset)
    btn4.pack()

    btn5 = Button(command_frame, text="Выйти", bg="white", font=40, command=close_program)
    btn5.pack()

    start()

    window.mainloop()
    
    
def create_output_window():
    global window
    global input_person_info, label_person_info, input_start_date_and_time, input_final_date_and_time, label_persons_list
    global input_now_name, input_new_name
    global tree

    window = Tk()
    window.wm_title("Face recognition")
    window.config(background="#FFFFFF")

    command_frame = Frame(window, width=600, height=500)
    command_frame.grid(row=800, column=0, padx=10, pady=2)

    title4 = Label(command_frame, text="Вывод информации об идентифицированном человеке", font=('Helvetica', 14, 'bold'))
    title4.pack()
    title5 = Label(command_frame, text="Введите имя", bg="white", font=40)
    title5.pack()
    input_person_info = Entry(command_frame, bg="white")
    input_person_info.pack()
    btn2 = Button(command_frame, text="Вывести информацию", bg="white", font=40, command=person_information)
    btn2.pack()
    label_person_info = Label(command_frame)
    label_person_info.pack()

    title6 = Label(command_frame, text="Вывод списка идентифицированных людей, которые были распознаны камерой за определенный промежуток времени /\nВывод статистики за определенный промежуток времени", font=('Helvetica', 14, 'bold'))
    title6.pack()
    title7 = Label(command_frame, text="Введите дату и время начала в формате YYYY-MM-DD HH:MM:SS (время указывать не обязательно)", bg="white", font=40)
    title7.pack()
    input_start_date_and_time = Entry(command_frame, bg="white")
    input_start_date_and_time.pack()
    title8 = Label(command_frame, text="Введите дату и время конца в формате YYYY-MM-DD HH:MM:SS (время указывать не обязательно)",bg="white", font=40)
    title8.pack()
    input_final_date_and_time = Entry(command_frame, bg="white")
    input_final_date_and_time.pack()
    btn3 = Button(command_frame, text="Вывести список идентифицированных людей", bg="white", font=40, command=recognized_persons_in_time_interval)
    btn3.pack()
    label_persons_list = Label(command_frame)
    label_persons_list.pack()
    btn4 = Button(command_frame, text="Вывести статистику", bg="white", font=40,command=statistics)
    btn4.pack()
    columns = ("1", "2", "3", "4", "5")
    tree = ttk.Treeview(command_frame, columns=columns, show="headings")
    tree.pack()

    btn5 = Button(command_frame, text="Очистить базу данных", bg="white", font=40, command=delete_dataset)
    btn5.pack()

    btn6 = Button(command_frame, text="Выйти", bg="white", font=40, command=close_program)
    btn6.pack()

    window.mainloop()


global window, main_label, dialog_label, cap
global input_name_reg, input_email_reg, input_pass1_reg, input_pass2_reg, label_reg, input_authorize_email, input_authorize_pass, label_authorize
global input_person_name_in_front_of_camera, input_now_name, input_new_name
global input_person_info, label_person_info, input_start_date_and_time, input_final_date_and_time, label_persons_list
global tree

if not os.path.isdir("dataset"):
    os.makedirs("dataset")

create_table_identified_persons()
create_table_unidentified_persons()
create_table_images()
create_table_access_data()
create_table_types_of_changes()
insert_types_of_changes()
create_table_total_system_statistics()

last_time = time.time()
new_time = time.time()

name_now = ""
number_of_persons_in_front_of_the_camera = 0

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

create_authorization_window()
