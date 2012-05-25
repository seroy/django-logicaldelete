from django.db import models


class LogicalDeleteOptions(object):
    """
    Options class for LogicalDeleteModelBase.
    """

    delete_related = True
    safe_deletion = True
    delete_batches = False

    def __init__(self, opts):
        if opts:
            for key, value in opts.__dict__.iteritems():
                setattr(self, key, value)


class LogicalDeleteModelBase(models.base.ModelBase):
    """
    BaseLogicalDelete metaclass.

    This metaclass parses LogicalDeleteOptions.
    """

    def __new__(cls, name, bases, attrs):
        new = super(LogicalDeleteModelBase, cls).__new__(cls, name, bases, attrs)
        logicaldelete_opts = attrs.pop('LogicalDeleteMeta', None)
        setattr(new, '_logicaldelete_meta', LogicalDeleteOptions(logicaldelete_opts))
        new._meta.permissions += (("undelete_%s" % new._meta.module_name,
                                   u'Can undelete %s' % new._meta.verbose_name_raw),)
        return new
