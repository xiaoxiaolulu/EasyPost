from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore as _SQLAlchemyJobStore
from apscheduler.jobstores.base import (
    JobLookupError,
    ConflictingIdError
)
from apscheduler.util import (
    maybe_ref,
    datetime_to_utc_timestamp
)
from datetime import datetime

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
    Jobs_History_Tablename = 'apscheduler_history'

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
            Column('next_run_time', Float(25), index=True),
            Column('job_state', LargeBinary, nullable=False),
            Column('trigger', String(256), nullable=True),
            Column('desc', String(256), nullable=True),
            schema=tableschema
        )
        self.jobs_t_history = Table(
            self.Jobs_History_Tablename, metadata,
            Column('id', BigInteger(), primary_key=True),
            Column('job_id', Unicode(191)),
            Column('run_time', DATETIME(), index=True, nullable=False),
            Column('is_error', Boolean(), default=0),
            Column('error_msg', String(256), nullable=True),
            schema=tableschema
        )

    def start(self, scheduler, alias):
        """
        Start the scheduler
        """
        super(SQLAlchemyJobStore, self).start(scheduler, alias)
        self.jobs_t.create(self.engine, True)
        self.jobs_t_history.create(self.engine, True)

    def add_job(self, job):
        """
        Add job object
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
        Update the job
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
        Get task rules and descriptions
        """
        the_type, rules = str(job.trigger).split('[')
        rule = rules.split(']')[0]
        trigger = '每隔'  # 定时任务的定时规则
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
        Insert historical task data
        """
        insert = self.jobs_t_history.insert().values(**{
            'job_id': data.get('job_id'),
            'run_time': data.get('run_time'),
            'is_error': data.get('is_error'),
            'error_msg': data.get('error_msg')
        })
        with self.engine.begin() as connection:
            connection.execute(insert)

    def api_get_run_next(self):
        """
        Get the next run time for each task
        """
        search = self.jobs_t.select().filter_by()
        with self.engine.begin() as connection:
            results = connection.execute(search)

        ret_data = []

        for row in results:
            dic = {
                'job_id': row[0],
                'next_run': datetime.fromtimestamp(row[1]).strftime(Datetime_Format),
                'trigger': row[3],
                'desc': row[4]
            }
            ret_data.append(dic)
        return ret_data

    def api_get_run_history(self):
        """
        Get the last 10 records of successful runs of each task
        """

        job_data_list = self.api_get_run_next()
        ret_data = []
        for dic in job_data_list:
            job_id = dic.get('job_id')
            history_data = {
                'job_id': job_id,
                'run_time': [],
            }
            search = self.jobs_t_history.select().filter_by(is_error=0, job_id=job_id).order_by(text('-id')).limit(10)
            with self.engine.begin() as connection:
                results = connection.execute(search)
            for row in results:
                run_time = datetime.strftime(row[2], Datetime_Format)
                history_data['run_time'].append(run_time)
            ret_data.append(history_data)
        return ret_data

    def api_get_run_error(self):
        """
        Get the last 10 records of failed runs for each task
        """
        job_data_list = self.api_get_run_next()
        ret_data = []
        for dic in job_data_list:
            job_id = dic.get('job_id')
            history_data = {
                'job_id': job_id,
                'error_run': [],
            }
            search = self.jobs_t_history.select().filter_by(is_error=1, job_id=job_id).order_by(text('-id')).limit(5)
            with self.engine.begin() as connection:
                results = connection.execute(search)
            for row in results:
                id = row[0]
                job_id = row[1]
                run_time = datetime.strftime(row[2], Datetime_Format)
                is_error = row[3]
                error_msg = row[4]
                history_data['error_run'].append({
                    'run_time': run_time,
                    'error_msg': error_msg
                })
            ret_data.append(history_data)
        return ret_data

    def delete_before_run_history(self):
        """
        In the historical running record,
            Only the last 20 successful runs are kept for each task
            Only the last 20 failed runs are kept for each task
        """
        session = self.engine.connect()
        table_name = self.Jobs_History_Tablename
        job_data_list = self.api_get_run_next()
        for dic in job_data_list:
            job_id = dic.get('job_id')
            search_success = self.jobs_t_history.select().filter_by(is_error=0, job_id=job_id).order_by(text('-id'))
            search_error = self.jobs_t_history.select().filter_by(is_error=1, job_id=job_id).order_by(text('-id'))
            delete_ids_su = []
            delete_ids_err = []
            with self.engine.begin() as connection:
                results_su = connection.execute(search_success)
                results_err = connection.execute(search_error)

            for row in results_su:
                delete_ids_su.append(row[0])
            for row in results_err:
                delete_ids_err.append(row[0])
            if delete_ids_su:
                delete_ids_su = delete_ids_su[20:]
                delete_query = text(f"DELETE FROM {table_name} WHERE id IN :job_ids")
                session.execute(delete_query, {"job_ids": delete_ids_su})
                session.commit()
            if delete_ids_err:
                delete_ids_err = delete_ids_err[20:]
                delete_query = text(f"DELETE FROM {table_name} WHERE id IN :job_ids")
                session.execute(delete_query, {"job_ids": delete_ids_err})
                session.commit()
        session.close()
