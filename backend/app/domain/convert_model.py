from datetime import datetime

from typing import List


class StorePath(object):
    bucket: str
    name: str

    def to_dict(self):
        return vars(self)


class ConvertMetadata(object):
    invoice_number: str
    seller_name: str
    buyer_name: str
    item_count: int
    amount_net: float
    invoice_date: datetime

    def to_dict(self):
        result = vars(self)
        return result


class Component(object):
    type: str  # file, data
    role: str  # root_file(1), parsed(2) => user_edit(3), generated(10),
    status: str  # progress, done, outdated, modified?
    order: int  # see role(order)
    data: any
    filename: str
    store_path: StorePath

    def to_dict(self):
        result = vars(self)
        result['store_path'] = self.store_path.to_dict()
        return result


class Convert(object):
    id: str
    components: List[Component]
    name: str
    global_status: int
    date_created: datetime
    user_created: str
    source: str = 'form'
    company: str
    metadata: ConvertMetadata

    def to_dict(self):
        components_dict = []
        for comp in self.components:
            components_dict.append(comp.to_dict())
        result = vars(self)
        result['components'] = components_dict
        result['metadata'] = self.metadata.to_dict()
        return result
