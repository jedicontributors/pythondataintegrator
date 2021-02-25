from typing import List

from models.viewmodels.operation.CreateDataOperationContactModel import CreateDataOperationContactModel
from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel


class CreateDataOperationModel:
    def __init__(self,
                 Name: str = None,
                 Contacts:List[CreateDataOperationContactModel]=None,
                 Integrations:List[CreateDataOperationIntegrationModel]=None,
                 *args, **kwargs):
        self.Name: str = Name
        self.Contacts: List[CreateDataOperationContactModel] = Contacts
        self.Integrations: List[CreateDataOperationIntegrationModel] = Integrations