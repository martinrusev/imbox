import datetime
from typing import Union


def format_date(date: Union[str, datetime.date]) -> str: ...

def build_search_query(**kwargs: Union[bool, str, datetime.date]) -> str: ...
