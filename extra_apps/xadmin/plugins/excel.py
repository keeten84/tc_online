# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/10/9 下午1:41'


import xadmin
from django.template import loader
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.plugins.utils import get_context_dict


# 自定义excel导入插件
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        # django2.0以上render_to_string的context需要传入字典，使用xadmin自带的 get_context_dict来转化
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',
                                             get_context_dict(context)))



xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)
