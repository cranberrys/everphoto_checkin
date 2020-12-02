from ac_api import AcApplication
from .handle.everphoto_api import EverPhoto
from .handle.handle_task import ECView, ec_task_action, ec_task_add, ec_task_smscode, ConfigView
from .handle.scheduler import auto_check_in


async def init_callback(app):
    app['ec_api'] = EverPhoto(app.request)
    with app.data_manager('cron_job') as cron_job:
        if not cron_job:
            cron_job.update({'hour': '21,23', 'minute': '0'})
        # cron_job.clear()
        # cron_job.update({'minute': '*/1', 'second': '0'})
        app.cron_job.add(key='auto_check_in', func=auto_check_in, **cron_job)


class EverphotoCheckin(AcApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ac_set_template_path('/template')
        self.ac_set_static_path('/static')

        self.router.add_view('/task', ECView, name='index')
        self.router.add_view('/config', ConfigView, name='config')
        self.router.add_get('/add', ec_task_add, name='ec_task_add')
        self.router.add_post('/action', ec_task_action, name='ec_task_action')
        self.router.add_post('/smscode', ec_task_smscode, name='ec_task_smscode')
        self.router.add_view('/task/{id}', ECView, name='ec_task_item')

        self.ac_set_init_callback(init_callback)


if __name__ == '__main__':
    everphoto_checkin().run()
