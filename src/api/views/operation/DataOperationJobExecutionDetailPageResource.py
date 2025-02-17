import json

from flask import make_response, request
from injector import inject

from IocManager import IocManager
from domain.operation.page.DataOperationJobExecutionDetailPage import DataOperationJobExecutionDetailPage
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.json.JsonConvert import JsonConvert
from views.operation.PageModels import PageModels


@PageModels.ns.route('/Job/Execution/<int:data_operation_job_execution_id>',doc=False)
class DataOperationJobExecutionDetailPageResource(ResourceBase):
    @inject
    def __init__(self, page: DataOperationJobExecutionDetailPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self,data_operation_job_execution_id):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(id=data_operation_job_execution_id,pagination=pagination)
        return make_response(page, 200)
