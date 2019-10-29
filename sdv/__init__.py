# -*- coding: utf-8 -*-
# configure logging for the library with a null handler (nothing is printed by default). See
# http://docs.pthon-guide.org/en/latest/writing/logging/

"""Top-level package for SDV."""

__author__ = """MIT Data To AI Lab"""
__email__ = 'dailabmit@gmail.com'
__version__ = '0.1.3-dev'


import json
import os

import pandas as pd

from sdv.metadata import Metadata
from sdv.modeler import Modeler
from sdv.sampler import Sampler
from sdv.sdv import SDV

__all__ = (
    'Metadata',
    'Modeler',
    'SDV',
    'Sampler',
)


def get_demo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.abspath(os.path.join(dir_path, '../examples/readme_demo'))

    tables = {
        'users': pd.read_csv(os.path.join(dir_path, 'users.csv')),
        'sessions': pd.read_csv(os.path.join(dir_path, 'sessions.csv')),
    }

    transactions = pd.read_csv(os.path.join(dir_path, 'transactions.csv'))
    transactions['datetime'] = pd.to_datetime(transactions['datetime'], format='%Y-%m-%d')

    tables['transactions'] = transactions

    with open(os.path.join(dir_path, 'metadata.json')) as metadata:
        metadata = json.load(metadata)

    return metadata, tables
