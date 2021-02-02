#!/usr/bin/python3

import os
import csv
import re

from xml.etree.ElementTree import ParseError
from xml.etree import ElementTree as ET  # noqa

from typing import Optional

from loguru import logger
import click

from converter import Payer, PayerList
from converter.files import move_file_to_directory, file_is_valid

CSV_FILE_NAME = 'register.csv'

logging_config = {
    'handlers': [
        {'sink': 'result.log'},
    ],
}

logger.configure(**logging_config)


def get_xml_encoding(file_content: bytes) -> str or None:
    """Get xml encoding"""
    encoding_value = re.compile(b'encoding=(.*?)\\?>').search(file_content)
    try:
        encoding = encoding_value.group(1).decode()
        xml_encoding = encoding.strip('\"').strip("\'")
    except AttributeError:
        return None
    return xml_encoding


def fill_list_of_payers_from_xml(xml_string: str, file_name: str) -> Optional[PayerList]:
    try:
        tree = ET.ElementTree(ET.fromstring(xml_string))
    except ParseError as e:
        logger.error(f'File error: {e}')
        return

    root = tree.getroot()

    main_part = root.find('СлЧаст')
    file_node = main_part.find('ОбщСвСч').find('ИдФайл')
    file_date = file_node.find('ДатаФайл').text

    info_part = root.find('ИнфЧаст')

    payers = PayerList()

    for index, item in enumerate(info_part, start=1):
        item_values = []
        for attribute in item:
            item_values.append(attribute.text)

        payer = Payer(index, file_name, file_date, *item_values).validate_values()

        if not payer:
            continue

        payers.append(payer)

    return payers


def create_register_of_payers(payers: PayerList, encoding: str, target_dir: str):

    csv_file_path = os.path.join(target_dir, CSV_FILE_NAME)

    with open(csv_file_path, 'w', newline='', encoding=encoding) as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for item in payers:
            writer.writerow(item[:10])


def get_file_content_and_encoding(file_path: str) -> (str, str) or (None, None):

    with open(file_path, 'rb') as xml_file:
        file_content: bytes = xml_file.read()
        encoding = get_xml_encoding(file_content)
        if not encoding:
            return None, None
        xml_string: str = file_content.decode(encoding)

    return xml_string, encoding


def create_csv_register(file_path: str):
    source_dir = os.path.dirname(file_path)
    source_name = os.path.basename(file_path)

    if not file_is_valid(file_path):
        move_file_to_directory(source_dir, source_name, source_dir, 'bad')
        return

    file_string, encoding = get_file_content_and_encoding(file_path=file_path)
    if not encoding:
        logger.error('Not found xml encoding.')
        return

    payers = fill_list_of_payers_from_xml(file_string, file_path)

    if not payers:
        return

    create_register_of_payers(payers, encoding, source_dir)
    move_file_to_directory(source_dir, source_name, source_dir, 'arh')


def move_log_file(file_path: str):
    source_dir = os.path.dirname(file_path)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    move_file_to_directory(current_dir, 'result.log', source_dir, 'log')


@click.command()
@click.argument('file_path')
def main(file_path: str) -> None:
    click.echo(f'Start register creating from file {file_path}...')
    create_csv_register(file_path)
    move_log_file(file_path)
    click.echo('Finish.For more information, see the logs.')


if __name__ == '__main__':
    main()
