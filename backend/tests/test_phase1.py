"""
Phase 1 Environment & Dependency Verification Test
Ensures all required machine learning, numerical, and API libraries load properly.
"""
import pytest

def test_ml_dependencies():
    import numpy as np
    import pandas as pd
    import scipy
    import sklearn
    import joblib
    import matplotlib
    import seaborn as sns

    assert np.__version__ is not None
    assert pd.__version__ is not None
    assert scipy.__version__ is not None
    assert sklearn.__version__ is not None
    assert joblib.__version__ is not None
    assert matplotlib.__version__ is not None
    assert sns.__version__ is not None

def test_api_dependencies():
    import fastapi
    import uvicorn
    import pydantic
    import sqlalchemy

    assert fastapi.__version__ is not None
    assert uvicorn.__version__ is not None
    assert pydantic.__version__ is not None
    assert sqlalchemy.__version__ is not None

def test_practical_packages_importable():
    import backend.ml.practical1
    import backend.ml.practical2
    import backend.ml.practical3
    import backend.ml.practical4
    import backend.ml.practical5
    import backend.ml.practical6
    import backend.ml.preprocessing
    import backend.app
