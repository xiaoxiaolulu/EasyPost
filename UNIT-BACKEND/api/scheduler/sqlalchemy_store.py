from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore as _SQLAlchemyJobStore
from apscheduler.jobstores.base import (
    JobLookupError,
    ConflictingIdError
)
from apscheduler.util import (
    maybe_ref,
    datetime_to_utc_timestamp
)

try:
    import cPickle as pickle # noqa
except ImportError:  # pragma: nocover
    import pickle

try:
    from sqlalchemy import (
        create_engine,
        Table,
        Column,
        MetaData,
        delete,
        Unicode,
        Float,
        LargeBinary,
        String,
        BigInteger,
        DATETIME,
        select,
        Boolean,
        text,
        and_
    )
    from sqlalchemy.exc import IntegrityError
    from sqlalchemy.sql.expression import null
except ImportError:  # pragma: nocover
    raise ImportError('SQLAlchemyJobStore requires SQLAlchemy installed')

Datetime_Format = '%Y-%m-%d %H:%M:%S'


class SQLAlchemyJobStore(_SQLAlchemyJobStore):

    Jobs_Tablename = 'apscheduler_jobs'

    def __init__(self, url=None, engine=None, metadata=None,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL, tableschema=None, engine_options=None):

        super(_SQLAlchemyJobStore, self).__init__()
        self.pickle_protocol = pickle_protocol
        metadata = maybe_ref(metadata) or MetaData()
        if engine:
            self.engine = maybe_ref(engine)
        elif url:
            self.engine = create_engine(url, **(engine_options or {}))
        else:
            raise ValueError('Need either "engine" or "url" defined')

        # 191 = max key length in MySQL for InnoDB/utf8mb4 tables,
        # 25 = precision that translates to an 8-byte float
        self.jobs_t = Table(
            self.Jobs_Tablename, metadata,
            Column('id', Unicode(191), primary_key=True),
            Column('job_state', LargeBinary, nullable=False),
            Column('status', String(256), nullable=True),
            Column('is_error', Boolean(), default=0),
            Column('error_msg', String(256), nullable=True),
            Column('trigger', String(256), nullable=True),
            Column('desc', String(256), nullable=True),
            Column('next_run_time', Float(25), index=True),
            Column('run_time', DATETIME(), index=True, nullable=True),
            schema=tableschema
        )

    def start(self, scheduler, alias):
        """
        Start the job store and perform any necessary initialization.

        Args:
            scheduler (Scheduler): The APScheduler instance this job store is attached to.
            alias (str, optional): An alias for this job store. Defaults to None.
        """
        super(SQLAlchemyJobStore, self).start(scheduler, alias)
        self.jobs_t.create(self.engine, True)

    def add_job(self, job):
        """
        Add a new job to the database.

        Args:
            job (Job): The APScheduler job object to be added.
        """

        trigger, desc = self.get_job_rule_and_desc(job)
        add_insert = self.jobs_t.insert().values(**{
            'id': job.id,
            'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
            'job_state': pickle.dumps(job.__getstate__(), self.pickle_protocol),
            'trigger': trigger,
            'desc': desc

        })
        with self.engine.begin() as connection:
            try:
                connection.execute(add_insert)
            except IntegrityError:
                raise ConflictingIdError(job.id)

    def update_job(self, job):
        """
        Update the state and details of an existing job in the database.

        Args:
            job (Job): The APScheduler job object with updated information.
        """
        trigger, desc = self.get_job_rule_and_desc(job)
        update = self.jobs_t.update().values(**{
            'next_run_time': datetime_to_utc_timestamp(job.next_run_time),
            'job_state': pickle.dumps(job.__getstate__(), self.pickle_protocol),
            'trigger': trigger,
            'desc': desc
        }).where(self.jobs_t.c.id == job.id)
        with self.engine.begin() as connection:
            result = connection.execute(update)
            if result.rowcount == 0:
                raise JobLookupError(job.id)

    @staticmethod
    def get_job_rule_and_desc(job):
        """
        Generate a human-readable trigger rule and description from an APScheduler job object.

        Args:
            job (Job): The APScheduler job object.

        Returns:
            tuple: A tuple containing the human-readable trigger rule (str) and job description (str).
        """
        the_type, rules = str(job.trigger).split('[')
        rule = rules.split(']')[0]
        trigger = '每隔'
        if the_type == 'date':
            # rule = '2024-10-10 20:20:12 csl'
            trigger = '在{} 时间点执行一次'.format(rule.rsplit(' ', 1)[0])
        elif the_type == 'interval':
            dic = {0: '小时', 1: '分钟', 2: '秒'}
            if 'day' in rule:
                # rule = '1 ady,00:00:00'
                day, hms = rule.split(',')
                day = int(day.split('day')[0])
                trigger += '{}天'.format(day)
                hms = hms.split(':')
            else:
                # rule = '01:01:01'
                hms = rule.split(':')
            for i, value in enumerate(hms):
                value = int(value)
                if value > 0:
                    trigger += str(value)
                    trigger += dic.get(i)
            else:
                trigger += '执行一次'
        else:
            # rule ="hour='0', minute='0', second='1'"
            trigger = '{},通过linux系统cron表达式'.format(job.trigger)
        desc = job.name or ''
        return (trigger, desc)

    def insert_job_history(self, data: dict):
        """
        Insert a new job history record into the database.

        Args:
            data (dict): A dictionary containing job history information.
                - job_id (str): The ID of the job the history belongs to.
                - run_time (str, optional): The timestamp of the job execution (default: current time).
                - is_error (int, optional): Flag indicating error (0 for success, 1 for error).
                - error_msg (str, optional): Error message if an error occurred.
                - status (str, optional): Job execution status (e.g., "SUCCESS", "FAILURE").
        """
        insert = self.jobs_t.update().values(**{
            'run_time': data.get('run_time'),
            'is_error': data.get('is_error'),
            'error_msg': data.get('error_msg'),
            'status': data.get('status')
        }).where(self.jobs_t.c.id == data.get('job_id'))
        with self.engine.begin() as connection:
            connection.execute(insert)
