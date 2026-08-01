
import requests
from typing import Optional
from shared.models.ImpulseCrmSearchColumn import ImpulseCrmSearchColumn
from shared.config.external_crm_config import BASE_URL, HEADERS

def fetch_get_list(method: str, page: int = 1, limit: int = 10, impulseCrmSearchColumn: Optional[ImpulseCrmSearchColumn] = None) -> dict:

    data: dict[str, any] = {
        #"fields": ["id", "lastName", "name", "middleName", "phone"],
        "limit" : limit,
        "page" : page,
        # "sort" : {
        #     "created" : "desc"
        # },
    }
    if impulseCrmSearchColumn is not None:
        data["columns"] = impulseCrmSearchColumn.to_dict()

    response = requests.post(url=f"{BASE_URL}/{method}", headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()