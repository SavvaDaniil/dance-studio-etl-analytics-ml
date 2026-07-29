


class ImpulseCrmSearchColumn:

    def __init__(self, visitDateFrom: int, visitDateTo: int):
        self.visitDateFrom = visitDateFrom
        self.visitDateTo = visitDateTo

    def to_dict(self) -> dict:
        # if self.visitDateFrom == 0 or self.visitDateTo == 0:
        #     return '{}'
        # return '{"visitDate" : {"from" : ' + str(self.visitDateFrom) + ', "to" : ' + str(self.visitDateTo) + '}}'
        return {
            "visitDate": {
                "from" : self.visitDateFrom,
                "to" : self.visitDateTo
            }
        }