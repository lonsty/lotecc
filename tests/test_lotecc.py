#!/usr/bin/env python

"""Tests for `lotecc` package."""
import os

import pytest

from click.testing import CliRunner

from lotecc import lotecc
from lotecc import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""

    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def test_s2t():
    """Test s2t."""

    input_file = 'tests/testcases/s2t.in'
    output_file = 'tests/testcases/s2t.out'
    input_ans = 'tests/testcases/s2t.ans'

    runner = CliRunner()
    conversion_result = runner.invoke(cli.main, ['-c', 's2t', '-i', input_file, '-o', output_file])
    assert conversion_result.exit_code == 0

    assert os.path.isfile(output_file)

    with open(output_file, 'r') as f:
        output_str = f.read().strip()
    with open(input_ans, 'r') as f:
        answer_str = f.read().strip()

    assert output_str == answer_str

    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass


def test_t2s():
    """Test t2s."""

    input_file = 'tests/testcases/t2s.in'
    output_file = 'tests/testcases/t2s.out'
    input_ans = 'tests/testcases/t2s.ans'

    runner = CliRunner()
    conversion_result = runner.invoke(cli.main, ['-c', 't2s', '-i', input_file, '-o', output_file])
    assert conversion_result.exit_code == 0

    assert os.path.isfile(output_file)

    with open(output_file, 'r') as f:
        output_str = f.read().strip()
    with open(input_ans, 'r') as f:
        answer_str = f.read().strip()

    assert output_str == answer_str

    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass


def test_lote_s2t():
    """Test lote s2t"""

    input_dir = 'tests/testcases'
    output_files = [
        'tests/testcases/s2t_c.ans',
        'tests/testcases/s2t_c.in',
        'tests/testcases/t2s_c.ans',
        'tests/testcases/t2s_c.in'
    ]
    answer_files = [
        'tests/testcases/s2t.ans',
        'tests/testcases/s2t.ans',
        'tests/testcases/t2s.in',
        'tests/testcases/t2s.in'
    ]

    runner = CliRunner()
    conversion_result = runner.invoke(cli.main, ['-i', input_dir, '--suffix', '_c'])
    assert conversion_result.exit_code == 0

    for idx, output_file in enumerate(output_files):
        assert os.path.isfile(output_file)

        # with open(output_file, 'r') as f:
        #     output_str = f.read().strip()
        # with open(answer_files[idx], 'r') as f:
        #     answer_str = f.read().strip()
        #
        # assert output_str == answer_str

        try:
            os.remove(output_file)
        except FileNotFoundError:
            pass
