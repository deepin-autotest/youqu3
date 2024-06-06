try:
    from youqu_dogtail import DogtailUtils as Dogtail

    HAS_DOGTAIL = True
except ImportError:
    HAS_DOGTAIL = False