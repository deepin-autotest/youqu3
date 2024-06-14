try:
    from youqu_dogtail import DogtailUtils as Dogtail

    HAS_DOGTAIL = True
except ImportError:
    HAS_DOGTAIL = False

if HAS_DOGTAIL is False:
    raise ImportError("youqu-dogtail is required, try 'pip install youqu-dogtail'")