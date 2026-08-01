

from shared.extract.crm_api import fetch_get_list

def branch_list() -> dict[str, list]:
    return fetch_get_list(method="branch/list")

if __name__ == "__main__":
    branch_data: dict[str, list] = branch_list()
    #print(abonements[0])