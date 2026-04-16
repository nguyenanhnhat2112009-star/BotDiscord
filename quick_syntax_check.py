import ast
import sys

def check_syntax():
    try:
        with open('Module/help.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        ast.parse(code)
        print("✅ Syntax OK!")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
            if e.offset:
                print(f"   {' ' * (e.offset - 1)}^")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if check_syntax():
        print("🚀 File is ready!")
    else:
        print("❌ Fix errors first!")
