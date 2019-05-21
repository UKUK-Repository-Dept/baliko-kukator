from sqlalchemy import and_, or_

class Utils(object):

    def __init__(self, db):
        """
        :param db: database session
        """
        self.__db = db
       
    def doc_stats(self):
        db = self.__db
        def count_started(uuid):
            where_started = and_(db.document.batch_uuid == uuid, db.document.state == 'started')
            count_started = len(db.document.filter(where_started).all())

            return count_started

        def count_planned(uuid):
            where_started = and_(db.document.batch_uuid == uuid, db.document.state == 'planned')
            count_planned = len(db.document.filter(where_started).all())

            return count_planned

        def count_finished(uuid):
            where_started = and_(db.document.batch_uuid == uuid, db.document.state == 'finished')
            count_finished = len(db.document.filter(where_started).all())

            return count_finished

        def count_failed(uuid):
            where_started = and_(db.document.batch_uuid == uuid, db.document.state == 'failed')
            count_failed = len(db.document.filter(where_started).all())

            return count_failed

        def count_all(uuid):
            count_all = len(db.document.filter_by(batch_uuid=uuid).all())
            return count_all

        return dict(count_started=count_started, count_failed=count_failed, count_planned=count_planned, 
                    count_finished=count_finished, count_all=count_all)

    def register_processors(self, app):
        app.context_processor(self.doc_stats)
