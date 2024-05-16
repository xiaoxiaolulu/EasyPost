from django.core.management.base import BaseCommand
from api.models.setting import Menu


class Command(BaseCommand):
    def handle(self, *args, **options):
        http_main_menu, created = Menu.objects.get_or_create(
            name='https',
            path='/https',
            component="Layout",
            redirect="/https/404",
            title="接口测试",
            icon="ElementPlus",
            parent_id=0
        )
        Menu.objects.get_or_create(
            name='apis',
            path='/https/apis',
            component="/https/api/index.vue",
            title="接口管理",
            icon="ElementPlus",
            parent_id=http_main_menu.id
        )
        Menu.objects.get_or_create(
            name='httpDetail',
            path='/https/detail',
            component="/https/api/components/detail.vue",
            title="接口详情",
            icon="ElementPlus",
            hidden=True,
            parent_id=http_main_menu.id
        )
        Menu.objects.get_or_create(
            name='case',
            path='/https/case',
            component="/https/case/index.vue",
            title="接口用例",
            icon="ElementPlus",
            parent_id=http_main_menu.id
        )
        Menu.objects.get_or_create(
            name='caseDetail',
            path='/case/detail',
            component="/https/case/components/detail.vue",
            title="接口详情",
            hidden=True,
            icon="ElementPlus",
            parent_id=http_main_menu.id
        )
        Menu.objects.get_or_create(
            name='plan',
            path='/https/plan',
            component="/https/plan/index.vue",
            title="测试计划",
            icon="ElementPlus",
            parent_id=http_main_menu.id,
        )
        Menu.objects.get_or_create(
            name='planDetail',
            path='/plan/detail',
            component="/https/plan/components/detail.vue",
            title="计划详情",
            icon="ElementPlus",
            parent_id=http_main_menu.id,
            hidden=True
        )

        project_main_menu, created = Menu.objects.get_or_create(
            name='project',
            path='/project',
            component="Layout",
            redirect="/project/404",
            title="项目管理",
            icon="ElementPlus",
            parent_id=0
        )
        Menu.objects.get_or_create(
            name='projectList',
            path='/plan/list',
            component="/project/index.vue",
            title="项目管理",
            icon="FolderRemove",
            parent_id=project_main_menu.id
        )
        Menu.objects.get_or_create(
            name='projectDetail',
            path='/project/detail',
            component="/project/components/editProject.vue",
            title="项目详情",
            icon="ElementPlus",
            hidden=True,
            parent_id=project_main_menu.id
        )

        record_main_menu, created = Menu.objects.get_or_create(
            name='record',
            path='/record',
            component="Layout",
            redirect="/record/404",
            title="测试报告",
            icon="ElementPlus",
            parent_id=0
        )
        Menu.objects.get_or_create(
            name='recordList',
            path='/record/list',
            component="/record/build/index.vue",
            title="构建历史",
            icon="ElementPlus",
            parent_id=record_main_menu.id
        )
        Menu.objects.get_or_create(
            name='recordDetail',
            path='/record/detail',
            component="/record/build/components/detail.vue",
            title="构建详情",
            icon="ElementPlus",
            hidden=True,
            parent_id=record_main_menu.id
        )
        Menu.objects.get_or_create(
            name='historyList',
            path='/history/list',
            component="/record/history/index.vue",
            title="执行记录",
            icon="ElementPlus",
            parent_id=record_main_menu.id
        )

        system_main_menu, created = Menu.objects.get_or_create(
            name='system',
            path='/system',
            component="Layout",
            redirect="/system/404",
            title="测试配置",
            icon="Setting",
            parent_id=0
        )
        Menu.objects.get_or_create(
            name='env',
            path='/system/environment',
            component="/system/env/index.vue",
            title="环境管理",
            icon="Eleme",
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='environmentDetail',
            path='/environment/detail',
            component="/system/env/components/detail.vue",
            title="环境管理详情",
            icon="AddLocation",
            hidden=True,
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='database',
            path='/system/database',
            component="/system/database/index.vue",
            title="数据库管理",
            icon="AddLocation",
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='datastructure',
            path='/system/datastructure',
            component="/system/datastructure/index.vue",
            title="数据结构",
            icon="AddLocation",
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='functionDetail',
            path='/function/detail',
            component="/system/function/components/detail.vue",
            title="内置函数详情",
            icon="AddLocation",
            hidden=True,
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='function',
            path='/system/function',
            component="/system/function/index.vue",
            title="内置函数",
            icon="AddLocation",
            parent_id=system_main_menu.id
        )
        Menu.objects.get_or_create(
            name='notice',
            path='/system/notice',
            component="/system/notice/index.vue",
            title="通知设置",
            icon="AddLocation",
            parent_id=system_main_menu.id
        )

        config_main_menu, created = Menu.objects.get_or_create(
            name='config',
            path='/config',
            component="Layout",
            redirect="/config/404",
            title="系统配置",
            icon="Setting",
            parent_id=0
        )
        Menu.objects.get_or_create(
            name='user',
            path='/system/user',
            component="/system/user/index.vue",
            title="用户管理",
            icon="AddLocation",
            parent_id=config_main_menu.id
        )
        Menu.objects.get_or_create(
            name='dept',
            path='/system/dept',
            component="/system/dept/index.vue",
            title="部门管理",
            icon="AddLocation",
            parent_id=config_main_menu.id
        )
        Menu.objects.get_or_create(
            name='role',
            path='/system/role',
            component="/system/role/index.vue",
            title="角色管理",
            icon="AddLocation",
            parent_id=config_main_menu.id
        )
        Menu.objects.get_or_create(
            name='menu',
            path='/system/menu',
            component="/system/menu/index.vue",
            title="菜单管理",
            icon="AddLocation",
            parent_id=config_main_menu.id
        )
        Menu.objects.get_or_create(
            name='dictionary',
            path='/system/dictionary',
            component="/system/dictionary/index.vue",
            title="字典管理",
            icon="AddLocation",
            parent_id=config_main_menu.id
        )
        self.stdout.write('菜单初始化成功！')
