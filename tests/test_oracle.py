#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import pytest

from pyway.dbms.database import factory
from pyway.dbms import oracle


@pytest.mark.oracle_test
def test_oracle_factory() -> None:
    """Test that the Oracle database adapter can be loaded by the factory."""
    cls = factory('oracle')
    assert cls is not None
    assert cls == oracle.Oracle
