import re

import pytest

from ansible_bender.db import generate_working_cont_name
from ansible_bender.utils import run_cmd, graceful_get


def test_run_cmd():
    assert "etc" in run_cmd(["ls", "-1", "/"], return_all_output=True)


@pytest.mark.parametrize("image_name,expected", (
    ("lojza", r"^lojza-\d{8}-\d{12}-cont$"),
    (
        "172.30.1.1:5000/myproject/just-built-ansible-bender:latest",
        r"^172-30-1-1-5000-myproject-just-built-ansible-bender-latest-\d{8}-\d{12}-cont$",
    ),
))
def test_gen_work_cont_name(image_name, expected):
    assert re.match(expected, generate_working_cont_name(image_name))


@pytest.mark.parametrize("inp,path,exp", (
    ({1: 2}, (1, ), 2),
    ({1: {2: 3}}, (1, 2), 3),
    ({1: {2: [2, 3]}}, (1, 2, 1), 3),
    ({1: {4: 3}}, (1, 2), None),
    (None, (1, 2), None),
    (object(), (1, "a"), None),
))
def test_graceful_g(inp, path, exp):
    assert graceful_get(inp, *path) == exp


def test_graceful_g_w_default():
    inp = {1: {2: 3}}
    assert graceful_get(inp, 3, default="asd") == "asd"
    assert graceful_get(inp, 1, default="asd") == {2: 3}
    assert graceful_get(inp, 1, 2, default="asd") == 3
    assert graceful_get(inp, 1, 2, 4, default="asd") == "asd"
