from typing import List
from models.base.EntityBase import EntityBase
from models.base.operation.DataOperationContactBase import DataOperationContactBase
from models.base.operation.DataOperationJobBase import DataOperationJobBase
from models.base.operation.DataOperationIntegrationBase import DataOperationIntegrationBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataOperationBase(EntityBase):
    def __init__(self,
                 DefinitionId: int = None,
                 Name: str = None,
                 Definition=None,
                 DataOperationJobs: List[DataOperationJobBase] = [],
                 Integrations: List[DataOperationIntegrationBase] = [],
                 Contacts: List[DataOperationContactBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Contacts = Contacts
        self.Integrations = Integrations
        self.DataOperationJobs = DataOperationJobs
        self.DefinitionId: int = DefinitionId
        self.Name: str = Name
        self.Definition = Definition
