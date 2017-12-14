from django.db.models.lookups import GreaterThanOrEqual, LessThanOrEqual

from django.contrib.postgres.fields import ArrayField


@ArrayField.register_lookup
class ArrayGreaterThanOrEqual(GreaterThanOrEqual):
    def as_sql(self, qn, connection):
        sql, params = super(ArrayGreaterThanOrEqual, self).as_sql(qn, connection)
        sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
        return sql, params


@ArrayField.register_lookup
class ArrayLessThanOrEqual(LessThanOrEqual):
    def as_sql(self, qn, connection):
        sql, params = super(ArrayLessThanOrEqual, self).as_sql(qn, connection)
        sql = '%s::%s' % (sql, self.lhs.output_field.db_type(connection))
        return sql, params
