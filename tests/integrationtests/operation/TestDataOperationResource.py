from unittest import TestCase

from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata import DataOperationTestData


class TestDataOperationResource(TestCase):
    def __init__(self, methodName='TestDataOperationResource'):
        super(TestDataOperationResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_data_operation(self):
        expected = True
        self.test_manager.service_scenarios.create_test_connection(DataOperationTestData.test_integration_connection)
        try:
            response_data = self.test_manager.service_endpoints.insert_data_operation(
                DataOperationTestData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == DataOperationTestData.test_insert_input['Name']
            assert response_data['Result']['Integrations'][0]["Integration"]["Code"] == \
                   DataOperationTestData.test_insert_input['Integrations'][0]["Integration"]["Code"]
            assert response_data['Result']['Contacts'][0]["Email"] == \
                   DataOperationTestData.test_insert_input['Contacts'][0]["Email"]

            response_data = self.test_manager.service_endpoints.insert_data_operation(
                DataOperationTestData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == DataOperationTestData.test_update_input['Name']
            assert response_data['Result']['Integrations'][0]["Limit"] == \
                   DataOperationTestData.test_update_input['Integrations'][0]["Limit"]
            assert response_data['Result']['Integrations'][0]["ProcessCount"] == \
                   DataOperationTestData.test_update_input['Integrations'][0]["ProcessCount"]
            assert response_data['Result']['Contacts'][0]["Email"] == \
                   DataOperationTestData.test_update_input['Contacts'][0]["Email"]
            data_operation = self.test_manager.service_scenarios.get_data_operation(
                name=DataOperationTestData.test_insert_input['Name'])
            delete_request = {"Id": data_operation.Id}
            response_data = self.test_manager.service_endpoints.delete_data_operation(delete_request)
            assert response_data['Message'] == f'Data Operation removed successfully'

        except Exception as ex:
            assert True == False
        finally:
            # clean data_integration test operations
            pass
            # self.test_manager.service_scenarios.clear_operation(name=DataOperationTestData.test_insert_input['Name'])

    def test_data_operation_same_integration(self):
        expected = True
        self.test_manager.service_scenarios.create_test_connection(DataOperationTestData.test_integration_connection)
        response_data = self.test_manager.service_endpoints.insert_data_operation(
            DataOperationTestData.test_insert_input_same_integration_1)
        assert response_data['IsSuccess'] == expected

        data_operation_service = IocManager.injector.get(DataOperationService)
        data_operation = data_operation_service.get_by_name(
            DataOperationTestData.test_insert_input_same_integration_1["Name"])
        assert len(data_operation.Integrations) == 1
        assert data_operation.Integrations[0].DataIntegration.Code == \
               DataOperationTestData.test_insert_input_same_integration_1['Integrations'][0]["Integration"]["Code"]
        assert data_operation.Integrations[0].DataIntegration.Code == \
               response_data['Result']['Integrations'][0]["Integration"]["Code"]
        response_data = self.test_manager.service_endpoints.insert_data_operation(
            DataOperationTestData.test_insert_input_same_integration_2)
        assert response_data['IsSuccess'] == expected
        assert len(data_operation.Integrations) == 1
        assert data_operation.Integrations[0].DataIntegration.Code == \
               DataOperationTestData.test_insert_input_same_integration_2['Integrations'][0]["Integration"]["Code"]
        assert data_operation.Integrations[0].DataIntegration.Code == \
               response_data['Result']['Integrations'][0]["Integration"]["Code"]
