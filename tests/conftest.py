#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件
"""

import pytest
import tempfile
import os
from unittest.mock import Mock


@pytest.fixture
def temp_dir():
    """临时目录fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_args():
    """示例命令行参数"""
    args = Mock()
    args.paths = []
    args.ext = None
    args.task = None
    args.incremental = False
    args.interactive = False
    args.config_init = False
    args.config_show = False
    args.list_tasks = False
    args.list_extensions = False
    return args
