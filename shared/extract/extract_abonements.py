
from shared.extract.extract_branch import branch_list


def extract_abonements() -> dict[str, list]:
    """Загрузка абонементов и разовых из объекта филиала branch"""

    branch_data: dict = branch_list()
    if not branch_data["items"]:
        raise Exception("load_abonements \"items\" is empty")
    
    try:
        options = branch_data["items"][0]["options"]
        groupAccountTypes = options["groupAccountType"]
        groupSingleTypes = options["groupSingleType"]

    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid branch_data structure: {e}")
    
    return {
        "groupAccountTypes" : groupAccountTypes,
        "groupSingleTypes" : groupSingleTypes
    }