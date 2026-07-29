

from src.extract.crm_api import fetch_get_list

def load_branch() -> dict[str, list]:
    return fetch_get_list(method="branch/list")

if __name__ == "__main__":
    branch_data = load_branch()
    #print(abonements[0])