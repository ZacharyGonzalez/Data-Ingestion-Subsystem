from logger import make_logger

def test_make_logger():
    logger = None
    logger = make_logger()
    assert logger is not None