from block_import import block_imports, block_calls

block_imports(allowed_modules=["main.py", "bad_call.py"])

@block_calls(allowed_modules=["main.py"])
def booty_call():
    print("You called me!")    
