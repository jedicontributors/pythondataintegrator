from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_SCHEDULER_PAUSED, \
    EVENT_SCHEDULER_RESUMED, EVENT_EXECUTOR_ADDED, EVENT_EXECUTOR_REMOVED, EVENT_JOBSTORE_ADDED, EVENT_JOBSTORE_REMOVED, \
    EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, \
    EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, EVENT_JOB_MAX_INSTANCES
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from injector import inject

from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import ISingleton
from scheduler.JobSchedulerEvent import JobSchedulerEvent
from models.configs.ApsConfig import ApsConfig
from models.configs.DatabaseConfig import DatabaseConfig


class JobScheduler(ISingleton):
    @inject
    def __init__(self):
        self.scheduler: BackgroundScheduler = None

    def run(self):
        self.run_scheduler()
        print("job_process started")

    def run_scheduler(self):
        database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)
        database_config: DatabaseConfig = IocManager.injector.get(DatabaseConfig)
        aps_config: ApsConfig = IocManager.injector.get(ApsConfig)
        jobstores = {
            'default': SQLAlchemyJobStore(url=database_config.connection_string, tablename='ApSchedulerJobsTable',
                                          engine=database_session_manager.engine,
                                          metadata=IocManager.Base.metadata,
                                          tableschema='Aps')
        }
        executors = {
            'default': ThreadPoolExecutor(aps_config.thread_pool_executer_count),
            'processpool': ProcessPoolExecutor(aps_config.process_pool_executer_count)
        }
        job_defaults = {
            'coalesce': aps_config.coalesce,
            'max_instances': aps_config.max_instances
        }
        self.scheduler = BackgroundScheduler(daemon=True, jobstores=jobstores, executors=executors,
                                             job_defaults=job_defaults)

        JobSchedulerEvent.job_scheduler_type = JobScheduler
        self.scheduler.add_listener(JobSchedulerEvent.listener_finish, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_added, EVENT_JOB_ADDED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_submitted, EVENT_JOB_SUBMITTED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_removed, EVENT_JOB_REMOVED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_all_jobs_removed, EVENT_ALL_JOBS_REMOVED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_others,
                                    EVENT_JOB_MODIFIED | EVENT_JOB_MISSED | EVENT_JOB_MAX_INSTANCES)
        self.scheduler.add_listener(JobSchedulerEvent.listener_scheduler_other_events,
                                    EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN | EVENT_SCHEDULER_PAUSED |
                                    EVENT_SCHEDULER_RESUMED | EVENT_EXECUTOR_ADDED | EVENT_EXECUTOR_REMOVED |
                                    EVENT_JOBSTORE_ADDED | EVENT_JOBSTORE_REMOVED)

        JobSchedulerEvent.create_event_handler()
        self.scheduler.start()
        self.scheduler.print_jobs()

    def shutdown(self):
        self.scheduler.shutdown()

    def add_job_with_date(self, job_function, run_date, args=None, kwargs=None) -> Job:
        aps_config: ApsConfig = IocManager.injector.get(ApsConfig)
        job: Job = self.scheduler.add_job(job_function, 'date', run_date=run_date,
                                          misfire_grace_time=aps_config.default_misfire_grace_time_date_job, args=args,
                                          kwargs=kwargs)
        return job

    def add_job_with_cron(self, job_function, cron: CronTrigger, args=None, kwargs=None) -> Job:
        aps_config: ApsConfig = IocManager.injector.get(ApsConfig)
        job: Job = self.scheduler.add_job(job_function, cron,
                                          misfire_grace_time=aps_config.default_misfire_grace_time_cron_job, args=args,
                                          kwargs=kwargs)
        return job

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def modify_job(self, job_id, job_store=None, **changes):
        return self.scheduler.modify_job(job_id, job_store, **changes)

    def reschedule_job(self, job_id, job_store=None, trigger=None, **trigger_args):
        return self.scheduler.reschedule_job(job_id, job_store, trigger, **trigger_args)

    def pause_job(self, job_id, job_store=None):
        return self.scheduler.pause_job(job_id, job_store)

    def resume_job(self, job_id, job_store=None):
        return self.scheduler.resume_job(job_id, job_store)

    def remove_job(self, job_id, job_store=None):
        self.scheduler.remove_job(job_id, job_store)

    def get_job(self, job_id):
        return self.scheduler.get_job(job_id)

    def get_jobs(self, job_store=None):
        return self.scheduler.get_jobs(job_store)
