import datetime
import random

import numpy as np
import pandas as pd

COUNTRIES = [
    'Bulgaria',
    'Canada',
    'France',
    'Germany',
    'Spain',
    'United States',
]

GENDERS = ['M', 'F', None]

DEVICE_TYPES = ['MOBILE', 'TABLET']

OPERATIVE_SYSTEMS = ['iOS', 'android', 'windows']


def _get_random_choices(choices, amount):
    return np.array([random.choice(choices) for _ in range(amount)])


def _get_datetime(amount):
    return np.array([
        datetime.date(random.randint(2016, 2018), random.randint(1, 12), random.randint(1, 28))
        for _ in range(amount)
    ])


def get_demo():

    users = pd.DataFrame({
        'user_id': np.array(range(10)),
        'country': _get_random_choices(COUNTRIES, 10),
        'gender': _get_random_choices(GENDERS, 10),
        'age': np.array([random.randint(18, 50) for _ in range(10)]),
    })

    sessions = pd.DataFrame({
        'session_id': np.array(range(10)),
        'user_id': np.array([random.randint(0, 9) for _ in range(10)]),
        'device_type': _get_random_choices(DEVICE_TYPES, 10),
        'operative_system': _get_random_choices(OPERATIVE_SYSTEMS),
    })

    transactions = pd.DataFrame({
        'transaction_id': np.array(range(10)),
        'session_id': np.array([random.randint(0, 9) for _ in range(10)]),
        'datetime': pd.to_datetime(_get_datetime(10)),
        'amount': np.array([round(random.random() * 1000, 2) for _ in range(10)]),
        'approved': _get_random_choices([True, False], 10),
    })

    metadata = {
        "path": "",
        "tables": [
            {
                "headers": True,
                "name": "users",
                "path": "users.csv",
                "primary_key": "user_id",
                "use": True,
                "fields": [
                    {
                        "name": "user_id",
                        "type": "id",
                        "subtype": "number"
                    },
                    {
                        "name": "country",
                        "type": "categorical",
                        "subtype": "categorical"
                    },
                    {
                        "name": "gender",
                        "type": "categorical",
                        "subtype": "categorical"
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "subtype": "integer"
                    }
                ]
            },
            {
                "headers": True,
                "name": "sessions",
                "path": "sessions.csv",
                "primary_key": "session_id",
                "use": True,
                "fields": [
                    {
                        "name": "session_id",
                        "type": "id",
                        "subtype": "number"
                    },
                    {
                        "name": "user_id",
                        "ref": {
                            "field": "user_id",
                            "table": "users"
                        },
                        "type": "id",
                        "subtype": "number"
                    },
                    {
                        "name": "device_type",
                        "type": "categorical",
                        "subtype": "categorical"
                    },
                    {
                        "name": "operative_system",
                        "type": "categorical",
                        "subtype": "categorical"
                    }
                ]
            },
            {
                "headers": True,
                "name": "transactions",
                "path": "transactions.csv",
                "primary_key": "transaction_id",
                "use": True,
                "fields": [
                    {
                        "name": "transaction_id",
                        "type": "id",
                        "subtype": "number"
                    },
                    {
                        "name": "session_id",
                        "ref": {
                            "field": "session_id",
                            "table": "sessions"
                        },
                        "type": "id",
                        "subtype": "number"
                    },
                    {
                        "name": "datetime",
                        "type": "datetime",
                        "format": "%Y-%m-%d"
                    },
                    {
                        "name": "amount",
                        "type": "number",
                        "subtype": "float"
                    },
                    {
                        "name": "approved",
                        "type": "categorical",
                        "subtype": "bool"
                    }
                ]
            }
        ]
    }

    tables = {
        'users': users,
        'sessions': sessions,
        'transactions': transactions
    }

    return metadata, tables
