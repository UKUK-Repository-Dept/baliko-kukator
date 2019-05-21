from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import and_, or_

def build_class(name, db):

    class NewClass(db):
        __tablename__ = str(name)

    NewClass.__name__ = str(name)

    return NewClass

class index(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("index.html")

def build_batches(db, name="Batches"):
    
    class batches(ModelView):

        def count_planned():
            where_planned = and_(db.document.batch_uuid == db.batch.uuid, db.document.state == 'planned')
            count_planned = len(db.document.filter(where_planned).all())

            return count_planned

        can_create = False
        can_delete = False
        can_edit = True
        can_export = True
        can_view_details = True
        column_display_pk = True
        details_modal = False
        details_template = 'admin/model/details_batch.html'

        column_searchable_list = ('name', 'state')
        column_default_sort = ('finished', True)
        column_list = ('name', 'created', 'finished', 'state')
        column_exclude_list = ('uuid', 'batch_process')
        column_details_list = ('uuid', 'name', 'created', 'finished', 'batch_process', 'document_stats')
        
        # documents = db.document
        
        # def count_started(uuid):
        #     where_started = and_(db.document.batch_uuid == uuid, db.document.state == 'started')
        #     count_started = len(db.document.filter(where_started).all())

        #     return count_started

        # def count_finished(self, context, model, name):
        #     where_finished = and_(db.document.batch_uuid == db.batch.uuid, db.document.state == 'finished')
        #     count_finished = len(db.document.filter(where_finished).all())

        #     return count_finished

        # def count_failed(self, context, model, name):
        #     where_failed = and_(db.document.batch_uuid == db.batch.uuid, db.document.state == 'failed')
        #     count_failed = len(db.document.filter(where_failed).all())
            
        #     return count_failed

        # column_formatters = {
        #     'Planned docs': count_planned,
        #     "Started docs": count_started,
        #     "Finished docs": count_finished,
        #     "Failed docs": count_failed
        # }

        # def get_column_names(self, only_columns, excluded_columns):
        #         only_columns.append('Planned docs')
        #         only_columns.append('Started docs')
        #         only_columns.append('Finished docs')
        #         only_columns.append('Failed docs')
        #         return super().get_column_names(only_columns, excluded_columns)
        
    batches_view = batches(db.batch, db.session, name=name)
    
    return batches_view

class documents(BaseView):
    pass