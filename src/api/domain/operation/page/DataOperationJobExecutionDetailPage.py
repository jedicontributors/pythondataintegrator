from injector import inject
from sqlalchemy import func

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnection
from models.dao.operation import DataOperationJob, DataOperationJobExecution, \
    DataOperationJobExecutionIntegration, DataOperationJobExecutionIntegrationEvent, DataOperationIntegration


class DataOperationJobExecutionDetailPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_job_execution(self, id, pagination=None):
        headers = [
            {'value': 'Execution Id'},
            {'value': 'Job Id'},
            {'value': 'Name'},
            {'value': 'Schedule Info'},
            {'value': 'Status'},
            {'value': 'Log'},
            {'value': 'Source Data Count'},
            {'value': 'Affected Row Count'},
            {'value': 'Execution Start Date'},
            {'value': 'Execution End Date'}
        ]

        def prepare_row(data: DataOperationJobExecution):
            # data_operation_job = data.DataOperationJob
            # last_update_date = None
            # if data_operation_job.LastUpdatedDate is not None:
            #     last_update_date = data_operation_job.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            # next_run_time = '-'
            # if data_operation_job.ApSchedulerJob is not None and data_operation_job.ApSchedulerJob.NextRunTime is not None:
            #     next_run_time = data_operation_job.ApSchedulerJob.NextRunTime
            # contacts = []
            # if data_operation_job.DataOperation.Contacts is not None and len(
            #         data_operation_job.DataOperation.Contacts) > 0:
            #     for contact in data_operation_job.DataOperation.Contacts:
            #         contacts.append(contact.Email)
            # contact_str = ';'.join(contacts)
            max_id = self.repository_provider.database_session_manager.session.query(
                func.max(DataOperationJobExecutionIntegration.Id)) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id)
            error_integration = self.repository_provider.get(DataOperationJobExecutionIntegration).first(Id=max_id)
            error_log = ''
            if error_integration is not None and error_integration.Log is not None:
                error_log = error_integration.Log.replace('\n', '<br />').replace('\t',
                                                                                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            total_source_data_count = self.repository_provider.database_session_manager.session.query(
                func.sum(DataOperationJobExecutionIntegration.SourceDataCount).label("SourceDataCount")) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id).first()[0]
            if total_source_data_count is None or total_source_data_count < 0:
                total_source_data_count = 0

            total_affected_row = self.repository_provider.database_session_manager.session.query(
                func.sum(DataOperationJobExecutionIntegrationEvent.AffectedRowCount).label("AffectedRowCount")) \
                .join(DataOperationJobExecutionIntegration.DataOperationJobExecutionIntegrationEvents) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id).first()[0]
            if total_affected_row is None or total_affected_row < 0:
                total_affected_row = 0

            end_date = ''
            if data.EndDate is not None:
                end_date = data.EndDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            row = {
                'data':
                    [
                        {
                            'value': f'<a href="/DataOperation/Job/Execution/{data.Id}">{data.Id}</a>-<a href="/DataOperation/Job/Execution/Log/{data.Id}">log</a>'},
                        {
                            'value': f'<a href="/DataOperation/Job/{data.DataOperationJob.Id}">{data.DataOperationJob.Id}</a>'},
                        {
                            'value': f'<a href="/DataOperation/{data.DataOperationJob.DataOperation.Id}">{data.DataOperationJob.DataOperation.Name}({data.DataOperationJob.DataOperation.Id})</a>'},
                        {
                            'value': f'{data.DataOperationJob.Cron}({data.DataOperationJob.StartDate}-{data.DataOperationJob.EndDate})'},
                        {'value': data.Status.Description},
                        {'value': error_log},
                        {'value': total_source_data_count},
                        {'value': total_affected_row},
                        {'value': data.StartDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                         'class': 'mail-row-nowrap'},
                        {'value': end_date,
                         'class': 'mail-row-nowrap'}
                    ]
            }
            return row

        data_operation_job_execution_repository = self.repository_provider.get(DataOperationJobExecution)

        query = data_operation_job_execution_repository.filter_by(Id=id)
        # pagination.PageUrl = '/DataOperation/Job/Execution{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render_job_execution_integration(self, id, pagination=None):
        headers = [
            {'value': 'Order'},
            {'value': 'Code'},
            {'value': 'Source'},
            {'value': 'Target'},
            {'value': 'Status'},
            {'value': 'Start Date'},
            # {'value': 'End Date'},
            {'value': 'Limit'},
            {'value': 'Process Count'},
            {'value': 'Source Data Count'},
            {'value': 'Affected Row Count'},
            {'value': 'Log'}
        ]

        def prepare_row(data: DataOperationJobExecution):
            # data_operation_job = data.DataOperationJob
            # last_update_date = None
            # if data_operation_job.LastUpdatedDate is not None:
            #     last_update_date = data_operation_job.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            # next_run_time = '-'
            # if data_operation_job.ApSchedulerJob is not None and data_operation_job.ApSchedulerJob.NextRunTime is not None:
            #     next_run_time = data_operation_job.ApSchedulerJob.NextRunTime
            # contacts = []
            # if data_operation_job.DataOperation.Contacts is not None and len(
            #         data_operation_job.DataOperation.Contacts) > 0:
            #     for contact in data_operation_job.DataOperation.Contacts:
            #         contacts.append(contact.Email)
            # contact_str = ';'.join(contacts)
            job_execution_integration = data.DataOperationJobExecutionIntegration
            data_integration_id = job_execution_integration.DataOperationIntegration.DataIntegration.Id
            source_connection = self.repository_provider.get(DataIntegrationConnection).table \
                .filter(DataIntegrationConnection.IsDeleted == 0) \
                .filter(DataIntegrationConnection.DataIntegrationId == data_integration_id) \
                .filter(DataIntegrationConnection.SourceOrTarget == 0) \
                .one_or_none()
            target_connection = self.repository_provider.get(DataIntegrationConnection).table \
                .filter(DataIntegrationConnection.IsDeleted == 0) \
                .filter(DataIntegrationConnection.DataIntegrationId == data_integration_id) \
                .filter(DataIntegrationConnection.SourceOrTarget == 1) \
                .one_or_none()
            source_data_count = 0
            if job_execution_integration.SourceDataCount is not None and job_execution_integration.SourceDataCount > 0:
                source_data_count = job_execution_integration.SourceDataCount
            total_affected_row_count = 0
            for event in job_execution_integration.DataOperationJobExecutionIntegrationEvents:
                if event.AffectedRowCount is not None and event.AffectedRowCount > 0:
                    total_affected_row_count = total_affected_row_count + event.AffectedRowCount
            source_connection_name = source_connection.Connection.Name if source_connection is not None else ''
            target_connection_name = target_connection.Connection.Name if target_connection is not None else ''

            row = {
                "data": [
                    {'value': job_execution_integration.DataOperationIntegration.Order},
                    {'value': job_execution_integration.DataOperationIntegration.DataIntegration.Code},
                    {'value': source_connection_name},
                    {'value': target_connection_name},
                    {'value': job_execution_integration.Status.Description},
                    {'value': job_execution_integration.StartDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3] + '',
                     'class': 'mail-row-nowrap'
                     },
                    # {'value': job_execution_integration.EndDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                    #  },
                    {'value': job_execution_integration.Limit},
                    {'value': job_execution_integration.ProcessCount},
                    {'value': source_data_count},
                    {'value': total_affected_row_count},
                    {'value': job_execution_integration.Log}
                ]
            }
            return row

        query = self.repository_provider.create().session.query(
            DataOperationJobExecutionIntegration, DataOperationIntegration
        ) \
            .filter(DataOperationJobExecutionIntegration.DataOperationIntegrationId == DataOperationIntegration.Id) \
            .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == id) \
            .order_by(DataOperationIntegration.Order)
        # pagination.PageUrl = '/DataOperation/Job/Execution/' + id + '{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"DataOperationJobExecutionIntegration"."Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, id, pagination: Pagination):
        if pagination is None:
            pagination = Pagination(Limit=50)
        elif pagination.Limit is None:
            pagination.Limit = 50
        table_job_execution = self.render_job_execution(id)
        table_job_execution_integration = self.render_job_execution_integration(id)
        return self.html_template_service.render_html(
            content=f'''  
            <div style="font-size: 24px;"><b>Job Execution </b></div>
            {table_job_execution}
            <div style="font-size: 24px;"><b>Job Execution Integration </b></div>
            {table_job_execution_integration}''')
