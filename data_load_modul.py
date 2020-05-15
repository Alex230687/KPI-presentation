import os
import datetime
import xlrd
import sqlite3


def scale_table_load(workbook):
    worksheet = workbook.sheet_by_name('SCALE')
    data = []
    for row in range(1, worksheet.nrows):
        indicator = int(worksheet.cell(row, 0).value)
        position = int(worksheet.cell(row, 1).value)
        year = int(worksheet.cell(row, 2).value)
        percent_min = float(worksheet.cell(row, 3).value)
        percent_max = float(worksheet.cell(row, 4).value)
        bonus_min = float(worksheet.cell(row, 5).value)
        bonus_max = float(worksheet.cell(row, 6).value)
        bonus_share = float(worksheet.cell(row, 7).value)
        account = int(worksheet.cell(row, 8).value)
        data.append({
           'indicator': indicator,
           'row_position': position,
           'year': year,
           'percent_min': percent_min,
           'percent_max': percent_max,
           'bonus_min': bonus_min,
           'bonus_max': bonus_max,
           'bonus_share': bonus_share,
           'account': account
        })

    query_insert = """
        INSERT INTO main_scale (indicator_id, row_position, year, percent_min, percent_max, bonus_min, bonus_max,
            bonus_share, account_id)
        SELECT :indicator, :row_position, :year, :percent_min, :percent_max, :bonus_min, :bonus_max, :bonus_share,
            :account
        WHERE NOT EXISTS 
            (SELECT * FROM main_scale WHERE indicator_id=:indicator AND row_position=:row_position
            AND year=:year AND account_id=:account);
        """

    query_update = """
        UPDATE main_scale SET percent_min=:percent_min, percent_max=:percent_max, bonus_min=:bonus_min,
            bonus_max=:bonus_max, bonus_share=:bonus_share
            WHERE indicator_id=:indicator AND row_position=:row_position AND year=:year AND account_id=:account;
        """

    return query_insert, query_update, data


def target_table_load(workbook):
    worksheet = workbook.sheet_by_name('TARGET')
    data = []
    for row in range(1, worksheet.nrows):
        indicator = int(worksheet.cell(row, 0).value)
        year = int(worksheet.cell(row, 1).value)
        target = float(worksheet.cell(row, 2).value) if worksheet.cell(row, 2).value else 0
        data.append({
            'indicator': indicator,
            'year': year,
            'target': target
            })

    query_insert = """
        INSERT INTO main_target (indicator_id, year, target)
        SELECT :indicator, :year, :target
        WHERE NOT EXISTS
            (SELECT * FROM main_target WHERE indicator_id=:indicator AND year=:year);
        """

    query_update = "UPDATE main_target SET target=:target WHERE indicator_id=:indicator AND year=:year;"

    return query_insert, query_update, data


def report_table_load(workbook):
    worksheet = workbook.sheet_by_name('REPORT 2019')
    data = []
    for i in range(1, worksheet.nrows):
        row_code = int(worksheet.cell(i, 1).value) if worksheet.cell(i, 1).value else None
        row_position = int(worksheet.cell(i, 2).value) if worksheet.cell(i, 2).value else None
        org_code = int(worksheet.cell(i, 3).value) if worksheet.cell(i, 3).value else None
        numerator = int(worksheet.cell(i, 4).value) if worksheet.cell(i, 4).value else None
        denominator = int(worksheet.cell(i, 5).value) if worksheet.cell(i, 5).value else None
        year = int(worksheet.cell(i, 6).value)
        indicator = int(worksheet.cell(i, 0).value)
        data.append({
            'row_code': row_code,
            'row_position': row_position,
            'org_code': org_code,
            'numerator': numerator,
            'denominator': denominator,
            'year': year,
            'indicator': indicator
            })

    query_insert = """
        INSERT INTO main_report (row_code_id, row_position, org_code_id, numerator, denominator, year, indicator_id)
        SELECT :row_code, :row_position, :org_code, :numerator, :denominator, :year, :indicator
        WHERE NOT EXISTS 
            (SELECT * FROM main_report WHERE indicator_id=:indicator AND year=:year AND row_code_id=:row_code
            AND org_code_id=:org_code);
        """

    query_update = """
        UPDATE main_report SET row_position=:row_position AND numerator=:numerator AND denominator=:denominator
            WHERE indicator_id=:indicator AND year=:year AND row_code_id=:row_code AND org_code_id=:org_code;
        """

    return query_insert, query_update, data


def indicator_table_load(workbook):
    worksheet = workbook.sheet_by_name('INDICATOR')
    data = []
    for i in range(1, worksheet.nrows):
        id = int(worksheet.cell(i, 0).value)
        name = worksheet.cell(i, 1).value
        slug = worksheet.cell(i, 4).value
        indicator_effect = int(worksheet.cell(i, 3).value)
        indicator_group = int(worksheet.cell(i, 2).value)
        data.append({
            'id': id,
            'name': name,
            'slug': slug,
            'indicator_effect': indicator_effect,
            'indicator_group': indicator_group
        })

    query_insert = """
        INSERT INTO main_indicator (id, name, slag, indicator_effect_id, indicator_group_id)
        SELECT :id, :name, :slug, :indicator_effect, :indicator_group
        WHERE NOT EXISTS
            (SELECT * FROM main_indicator WHERE id=:id);
        """

    query_update = """
        UPDATE main_indicator SET name=:name, slag=:slug, indicator_effect_id=:indicator_effect,
            indicator_group_id=:indicator_group WHERE id=:id;
        """

    return query_insert, query_update, data


def data_table_load(workbook, data_sheets):
    data = []
    for sheet in data_sheets:
        worksheet = workbook.sheet_by_name(sheet)
        for i in range(1, worksheet.nrows):
            row_id = int(worksheet.cell(i, 1).value)
            org_id = int(worksheet.cell(i, 2).value)
            data_type = int(worksheet.cell(i, 4).value)
            value = float(worksheet.cell(i, 5).value)
            date = xlrd.xldate_as_tuple(worksheet.cell(i, 3).value, workbook.datemode)
            period = datetime.date(date[0], date[1], date[2]).isoformat()
            data.append({
                'row_id': row_id,
                'org_id': org_id,
                'data_type': data_type,
                'value': value,
                'period': period,
            })

    query_insert = """
        INSERT INTO main_data (row_id, org_id, data_type_id, value, period)
        SELECT :row_id, :org_id, :data_type, :value, :period
        WHERE NOT EXISTS
            (SELECT * FROM main_data WHERE row_id=:row_id AND org_id=:org_id AND data_type_id=:data_type
            AND period=:period);
        """

    query_update = """
        UPDATE main_data SET value=:value WHERE row_id=:row_id AND org_id=:org_id AND data_type_id=:data_type
            AND period=:period;
        """

    return query_insert, query_update, data


def row_table_load(workbook):
    worksheet = workbook.sheet_by_name('ROW')
    data = []
    for i in range(1, worksheet.nrows):
        id = int(worksheet.cell(i, 1).value)
        name = worksheet.cell(i, 2).value
        row_type = int(worksheet.cell(i, 3).value)
        row_group1 = int(worksheet.cell(i, 4).value)
        row_group2 = int(worksheet.cell(i, 5).value)
        row_group3 = int(worksheet.cell(i, 6).value)
        data.append({
            'id': id,
            'name': name,
            'row_type': row_type,
            'row_group1': row_group1,
            'row_group2': row_group2,
            'row_group3': row_group3
            })

    query_insert = """
        INSERT INTO main_row (id, name, row_type_id, row_group1_id, row_group2_id, row_group3_id)
        SELECT :id, :name, :row_type, :row_group1, :row_group2, :row_group3
        WHERE NOT EXISTS
            (SELECT * FROM main_row WHERE id=:id);
        """

    query_update = """
        UPDATE main_row SET name=:name, row_type_id=:row_type, row_group1_id=:row_group1, row_group2_id=:row_group2,
            row_group3_id=:row_group3 WHERE id=:id;
        """

    return query_insert, query_update, data


def base_table_load(workbook, keys):
    """Base <two-row> tables load function."""
    worksheet = workbook.sheet_by_name(keys['sheet'])
    data = []
    for row in range(1, worksheet.nrows):
        id = int(worksheet.cell(row, 0).value)
        name = worksheet.cell(row, 1).value
        data.append({'id': id, 'name': name})

    query_insert = """
        INSERT INTO %(table)s (id, name)
        SELECT :id, :name
        WHERE NOT EXISTS
            (SELECT * FROM %(table)s WHERE id=:id);
        """ % keys

    query_update = "UPDATE %(table)s SET name=:name WHERE id=:id;" % keys

    return query_insert, query_update, data


first_queue_load = [
    {'sheet': 'ROW_TYPE', 'table': 'main_rowtype'},
    {'sheet': 'GROUP_1', 'table': 'main_rowgroup1'},
    {'sheet': 'GROUP_2', 'table': 'main_rowgroup2'},
    {'sheet': 'GROUP_3', 'table': 'main_rowgroup3'},
    {'sheet': 'ORGANIZATION', 'table': 'main_organization'},
    {'sheet': 'DATA_TYPE', 'table': 'main_datatype'},
    {'sheet': 'INDICATOR_GROUP', 'table': 'main_indicatorgroup'},
    {'sheet': 'INDICATOR_EFFECT', 'table': 'main_indicatoreffect'},
]


data_sheets = [
    'DATA 2018',
    'DATA 2019',
]


load_func_block = [
    row_table_load,
    indicator_table_load,
    report_table_load,
    target_table_load,
    scale_table_load
]


class SQLContextManager:
    def __init__(self, database):
        self.database = database

    def __enter__(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def sql_handler(query, data):
    with SQLContextManager(db_path) as cur:
        try:
            cur.executemany(query, data)
        except (sqlite3.DatabaseError, sqlite3.InterfaceError) as error:
            print('ERROR')
            print(error)
        else:
            print('SUCCESS')


def base_table_handler():
    workbook = xlrd.open_workbook(excel_path)
    for key_block in first_queue_load:
        query_insert, query_update, data = base_table_load(workbook, key_block)
        sql_handler(query_insert, data)
        sql_handler(query_update, data)


def main_table_handler():
    workbook = xlrd.open_workbook(excel_path)
    for func in load_func_block:
        query_insert, query_update, data = func(workbook)
        sql_handler(query_insert, data)
        sql_handler(query_update, data)


def data_table_handler():
    workbook = xlrd.open_workbook(excel_path)
    query_insert, query_update, data = data_table_load(workbook, data_sheets)
    sql_handler(query_insert, data)
    sql_handler(query_update, data)


db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'django_sub.xlsm')


def complex_data_load_modul():
    """Total data load to database."""
    base_table_handler()
    main_table_handler()
    data_table_handler()


if __name__ == '__main__':
    complex_data_load_modul()
