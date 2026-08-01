
from shared.extract.crm_api import fetch_get_list


def schedule_list() -> list:
    total: int = 0
    items: list = []
    limit_max: int = 100

    page: int = 0

    response_json: dict = fetch_get_list(method="schedule/list", page=1, limit=0)
    total = response_json["total"]
    #print(f"Найден total: {total}")
    while limit_max * page < total:
        page += 1
        #print(f"\tзапрос на страницу {page}")
        response_json = fetch_get_list(method="schedule/list", page=page, limit=limit_max)
        items.extend(response_json["items"])
    
    #print(f"len(items): {len(items)}")
    return items

if __name__ == "__main__":
    schedule_list()