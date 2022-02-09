def checkPIP():
    import subprocess
    try:
        import Cython
    except ImportError:
        subprocess.check_call(
            ["python3", '-m', 'pip', 'install', 'Cython'])

    try:
        import skimage
    except ImportError:
        subprocess.check_call(
            ["python3", '-m', 'pip', 'install', 'scikit-image'])

    try:
        import PIL
    except ImportError:
        subprocess.check_call(
            ["python3", '-m', 'pip', 'install', 'Pillow'])


    try:
        import pycocotools
    except ImportError:
        subprocess.check_call(
            ["python3", '-m', 'pip', 'install', 'pycocotools'])