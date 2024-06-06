try:
    from youqu_imagecenter_rpc import ImageCenter as _ImageCenter
    from youqu_imagecenter_rpc import setting as image_setting

    HAS_IMAGECENTER = False
except ImportError:
    HAS_IMAGECENTER = False
