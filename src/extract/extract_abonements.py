
from src.extract.load_branch import load_branch


def extract_abonements() -> dict[str, list]:
    """Загрузка абонементов и разовых из объекта филиала branch"""

    branch_data: dict = load_branch()
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