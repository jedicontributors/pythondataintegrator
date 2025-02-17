import signal
from unittest import TestCase

from apscheduler.events import EVENT_JOB_REMOVED

from IocManager import IocManager
from infrastructor.connection.queue.QueueProvider import QueueProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager

from models.dao.aps import ApSchedulerJobEvent, ApSchedulerEvent, ApSchedulerJob
from models.dao.operation import DataOperationJob


class TestTimeout(TestCase):
    def __init__(self, method_name='TestTimeout'):
        super(TestTimeout, self).__init__(method_name)
        IocManager.initialize()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    @staticmethod
    def loop_forever():
        import time
        while 1:
            print("sec")
            time.sleep(1)

    @staticmethod
    def handler(signum, frame):
        print("Forever is over!")
        raise Exception("end of time")

    def test_timeout(self):
        signal.signal(signal.SIGALRM, TestTimeout.handler)
        signal.alarm(10)
        try:
            TestTimeout.loop_forever()
        except Exception as exc:
            print(exc)
        finally:
            signal.alarm(0)

    def test_consume_data(self):
        queue_provider = IocManager.injector.get(QueueProvider)
        context = queue_provider.get_context()
        data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
                                limit=100)
        assert len(data) <= 100

    def test_consume_all_data(self):
        queue_provider = IocManager.injector.get(QueueProvider)
        context = queue_provider.get_context()
        data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
                                limit=100)
        assert len(data) <= 100

    def test_sqlalchemy(self):
        database_session_manager = IocManager.injector.get(DatabaseSessionManager)
        # test_repo: Repository[ConfigParameter] = Repository[ConfigParameter](database_session_manager)
        # data = test_repo.table \
        #     .filter(ConfigParameter.Name.contains('EMAIL_HOST'))
        # for d in data:
        #     print(d)
        #
        # log_repo: Repository[Log] = Repository[Log](database_session_manager)
        # data = log_repo.table \
        #     .filter(Log.JobId == 356) \
        #     .filter(Log.Content.contains("CrmCustomerOperation")).all()
        #
        # for d in data:
        #     print(d)
        result = database_session_manager.session.query(
            DataOperationJob,ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
        ) \
            .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
            .filter(DataOperationJob.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
            .filter(ApSchedulerJob.JobId == '13b6cd62460b405fa8051b5ec9fafa6e')
        all_result = result.one_or_none()
        if all_result is not None:
            print(all_result.ApSchedulerEvent.Name)
        result = database_session_manager.session.query(
            ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
        ) \
            .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
            .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
            .filter(ApSchedulerJob.Id == 425)
        all_result = result.all()
        for r in result:
            print(r)
