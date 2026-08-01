
from shared.extract.crm_api import fetch_get_list
from shared.models.ImpulseCrmSearchColumn import ImpulseCrmSearchColumn
from requests.exceptions import ChunkedEncodingError, HTTPError
import time

def group_singles_list(visit_date_from: int, visit_date_to: int) -> list[dict]:
    total: int = 0
    items: list = []
    limit_max: int = 500

    page: int = 0
    impulseCrmSearchColumn: ImpulseCrmSearchColumn = ImpulseCrmSearchColumn(
        visitDateFrom=visit_date_from, 
        visitDateTo=visit_date_to
    )

    response_json: dict = fetch_get_list(method="group_single/list", page=1, limit=0, impulseCrmSearchColumn=impulseCrmSearchColumn)
    total = response_json["total"]
    print(f"Найдено group_singles total: {total}")

    retries: int = 5
    while limit_max * page < total:
        page += 1
        retries = 1
        while retries < 6:
            try:
                print(f"\tзапрос на страницу {page} попытка {retries}")
                response_json = fetch_get_list(method="group_single/list", page=page, limit=limit_max, impulseCrmSearchColumn=impulseCrmSearchColumn)
                items.extend(response_json["items"])
                break
            except ChunkedEncodingError:
                retries += 1
                time.sleep(5)
            except HTTPError:
                retries += 1
                time.sleep(5)
    
    #print(f"len(items): {len(items)}")
    return items