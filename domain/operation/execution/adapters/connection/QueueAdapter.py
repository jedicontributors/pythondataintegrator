from typing import List

from injector import inject
import pandas as pd
from pandas import DataFrame

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from infrastructor.connection.queue.QueueProvider import QueueProvider
from infrastructor.exceptions.NotSupportedFeatureException import NotSupportedFeatureException
from models.dto.PagingModifier import PagingModifier


class QueueAdapter(ConnectionAdapter):
    @inject
    def __init__(self,
                 queue_provider: QueueProvider,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 data_integration_column_service: DataIntegrationColumnService,
                 ):
        self.queue_provider = queue_provider
        self.data_integration_column_service = data_integration_column_service
        self.data_integration_connection_service = data_integration_connection_service

    def clear_data(self, data_integration_id) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_context = self.queue_provider.get_context(connection=target_connection.Connection)
        target_context.delete_topic(topic_name=target_connection.Queue.TopicName)
        target_context.create_topic(topic_name=target_connection.Queue.TopicName)
        return 1

    def get_source_data_count(self, data_integration_id) -> int:
        raise NotSupportedFeatureException("Queue Target Operation")
        # source_connection = self.data_integration_connection_service.get_source_connection(
        #     data_integration_id=data_integration_id)
        #
        # source_file_context = self.queue_provider.get_context(connection=source_connection.Connection)
        # file_path = os.path.join(source_connection.File.Folder, source_connection.File.FileName)
        # data_count = source_file_context.get_data_count(file=file_path)
        # if source_connection.File.Csv.HasHeader:
        #     data_count = data_count - 1
        # return data_count

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> DataFrame:
        raise NotSupportedFeatureException("File Target Operation")
        # source_connection = self.data_integration_connection_service.get_source_connection(
        #     data_integration_id=data_integration_id)
        # source_file_context = self.queue_provider.get_context(connection=source_connection.Connection)
        #
        # data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
        #     data_integration_id=data_integration_id)
        # has_header = None
        # if source_connection.File.Csv.HasHeader:
        #     has_header = 0
        # headers = None
        # if source_connection.File.Csv.Header is not None and source_connection.File.Csv.Header != '':
        #     headers = source_connection.File.Csv.Header.split(source_connection.File.Csv.Separator)
        #
        # file_path = os.path.join(source_connection.File.Folder, source_connection.File.FileName)
        # readed_data = source_file_context.get_data(file=file_path,
        #                                            names=headers,
        #                                            header=has_header,
        #                                            start=paging_modifier.Start,
        #                                            limit=paging_modifier.Limit,
        #                                            separator=source_connection.File.Csv.Separator)
        # column_names = [(data_integration_column.SourceColumnName) for data_integration_column in
        #                 data_integration_columns]
        # data = readed_data[column_names]
        # replaced_data = data.where(pd.notnull(data), None)
        # return replaced_data.values.tolist()

    def prepare_data(self, data_integration_id: int, source_data: List[any]) -> List[any]:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_context = self.queue_provider.get_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_data = target_context.prepare_insert_row(data=source_data, column_rows=column_rows)
        return prepared_data

    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_context = self.queue_provider.get_context(connection=target_connection.Connection)
        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)
        columns = [(data_integration_column.TargetColumnName) for data_integration_column in
                   data_integration_columns]
        data = pd.DataFrame(prepared_data, columns=columns)
        affected_row_count = target_context.write_data(
            topic_name=target_connection.Queue.TopicName, messages=data)
        return affected_row_count

    def do_target_operation(self, data_integration_id: int) -> int:
        raise NotSupportedFeatureException("Queue Target Operation")
