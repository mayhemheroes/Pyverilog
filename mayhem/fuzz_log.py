#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
from contextlib import contextmanager
import io

with atheris.instrument_imports(include=['pyverilog']):
    from pyverilog.vparser.parser import VerilogParser, ParseError

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

parser = VerilogParser()

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        parser.parse(fdp.ConsumeRemainingString())
    except ParseError:
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
