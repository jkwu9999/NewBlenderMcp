import bpy
import io
from contextlib import redirect_stdout

def execute_code(code):
    try:
        namespace = {"bpy": bpy}
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exec(code, namespace)
        return {"executed": True, "result": buffer.getvalue()}
    except Exception as e:
        raise Exception(f"Code execution error: {str(e)}")
