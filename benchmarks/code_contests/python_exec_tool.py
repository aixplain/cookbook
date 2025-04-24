import multiprocessing
import queue
import subprocess
import sys
import time
import traceback
from langchain.tools import StructuredTool
import re

multiprocessing.set_start_method("fork", force=True)
# WARNING
# This program exists to execute untrusted model-generated code. Although
# it is highly unlikely that model-generated code will do something overtly
# malicious in response to this test suite, model-generated code may act
# destructively due to a lack of model capability or alignment.
# Users are strongly encouraged to sandbox this evaluation suite so that it
# does not perform destructive actions on their host or network.
# Proceed at your own risk:
TOOL_DESCRIPTION = "A Python shell. Use this to execute python program."
INPUT_DESCRIPTION = """Input MUST be a JSON map with the following keys: {0}. The input MUST be in the following format: {1}."""


def exec_program(q, program, input_data, expected_output, timeout):
    try:
        start_time = time.time()
        process = subprocess.Popen(
            [sys.executable, "-c", program],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(input=input_data, timeout=timeout)
        if time.time() - start_time > timeout:
            raise TimeoutError("Execution timed out.")
        if process.returncode != 0:
            q.put(f"failed: {stderr}")
        else:
            if stdout.strip() == expected_output.strip():
                q.put("passed")
            else:
                q.put(f"wrong answer. Expected '{expected_output}', got '{stdout}'")
    except subprocess.TimeoutExpired:
        process.kill()
        q.put("timed out")
    except Exception:
        q.put(f"failed: {traceback.format_exc()}")


def get_code_from_output(response):
    try:
        code = re.findall(r"```python*(.*?)\s```", response, re.DOTALL)[0]
        return code
    except Exception as e:
        pass
    return None


def check_correctness(
    # query: dict
    program: str,
    input_data: str,
    expected_output: str,
    timeout: float,
    **kwargs,
) -> str:
    print(f"Kwargs: {kwargs}")
    code = get_code_from_output(program)
    if code is not None:
        program = code

    q = multiprocessing.Queue()
    process = multiprocessing.Process(target=exec_program, args=(q, program, input_data, expected_output, timeout))
    process.start()
    # process.join(timeout=query["timeout"] + 1)
    process.join(timeout=timeout + 1)
    if process.is_alive():
        process.terminate()
        process.join()
        result = "timed out"
    else:
        try:
            result = q.get_nowait()
        except queue.Empty:
            result = "no result returned"
    return result


def get_python_exec_tool():
    required_params = {
        "program": "str: the python code to be executed",
        "input_data": "str: input data",
        "expected_output": "str: expected output",
        "timeout": "float: time in seconds before the code execution times out",
    }
    function_inputs = "\n".join([f"{param}: {required_params[param]}" for param in required_params])
    description = INPUT_DESCRIPTION.format(
        # function_inputs, {"query": {param: "VALUE" for param in required_params}}, {param: "VALUE" for param in required_params}
        function_inputs,
        {param: "VALUE" for param in required_params},
    )
    definition = TOOL_DESCRIPTION + f" {description}"
    code_exec = StructuredTool.from_function(
        name="python_code_execution",
        description=definition,
        func=check_correctness,
    )
    return code_exec