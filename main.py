import os
import sys
import time
import zlib
import marshal
import base64
import random
import string
import hashlib
import subprocess
from colorama import Fore, init
import subprocess
import base64



layers = 5
junk_amount = 35

os.system("title BY kenwood")


logo = r"""
 ░██████   ░██████    ░████     ░██   
░██   ░██ ░██   ░██  ░██ ░██  ░████   
      ░██       ░██ ░██ ░████   ░██   
  ░█████    ░█████  ░██░██░██   ░██   
      ░██       ░██ ░████ ░██   ░██   
░██   ░██ ░██   ░██  ░██ ░██    ░██   
 ░██████   ░██████    ░████   ░██████ 
                                      
 VIRUS-TOTAL-BYPASS   dev by : kenwood
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def random_name(size=20):
    return "".join(random.choice(string.ascii_letters) for _ in range(size))


def loading():
    for i in range(1, 11):
        print(Fore.RED + f"\rLoading [{'#' * i}{'.' * (10-i)}]", end="")
        time.sleep(0.05)

    print("\n")


def create_junk():

    data = []

    for _ in range(junk_amount):

        var1 = random_name()
        var2 = random_name()

        number = random.randint(10000, 99999)

        data.append(f"{var1} = {number}")

        md5 = hashlib.md5(str(number).encode()).hexdigest()

        data.append(f"{var2} = '{md5}'")

    return "\n".join(data)


def make_oneline(encoded):

    return (
        "import marshal,zlib,base64;"
        f"exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"
    )


def obfuscate(code):

    current = code

    for _ in range(layers):

        compiled = compile(current, "<kenwood>", "exec")

        dumped = marshal.dumps(compiled)

        compressed = zlib.compress(dumped)

        encoded = base64.b64encode(compressed).decode()

        a = random_name()
        b = random_name()

        current = f"""
import marshal,zlib,base64

{create_junk()}

{a} = "{encoded}"

{b} = marshal.loads(
    zlib.decompress(
        base64.b64decode({a})
    )
)

exec({b})
"""

    return current


def obfuscate_only():

    clear()

    print(Fore.RED + logo)

    path = input(Fore.WHITE + "file path > ").strip()

    if not os.path.isfile(path):

        print(Fore.RED + "\nfile not found")
        input("\nenter to continue")
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        print(Fore.RED + "\nobfuscating...")
        loading()

        result = obfuscate(code)

        output = os.path.join(
            os.path.dirname(path),
            "obf_" + os.path.basename(path)
        )

        with open(output, "w", encoding="utf-8") as f:
            f.write(result)

        print(Fore.GREEN + f"\ndone -> {output}")

    except Exception as e:

        print(Fore.RED + f"\nerror: {e}")

    input(Fore.WHITE + "\nenter to continue")


def protect_file():

    clear()

    print(Fore.RED + logo)

    path = input(Fore.WHITE + "file path > ").strip()

    if not os.path.isfile(path):

        print(Fore.RED + "\nfile not found")
        input("\nenter to continue")
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        print(Fore.RED + "\nbuilding...")
        loading()

        protected = obfuscate(code)

        compiled = compile(protected, "<final>", "exec")

        dumped = marshal.dumps(compiled)

        compressed = zlib.compress(dumped)

        encoded = base64.b64encode(compressed).decode()

        final = make_oneline(encoded)

        output = os.path.join(
            os.path.dirname(path),
            "protected_" + os.path.basename(path)
        )

        with open(output, "w", encoding="utf-8") as f:
            f.write(final)

        print(Fore.GREEN + f"\nsaved -> {output}")

    except Exception as e:

        print(Fore.RED + f"\nerror: {e}")

    input(Fore.WHITE + "\nenter to continue")


def protect_and_build():

    clear()

    print(Fore.RED + logo)

    path = input(Fore.WHITE + "file path > ").strip()

    if not os.path.isfile(path):

        print(Fore.RED + "\nfile not found")
        input("\nenter to continue")
        return

    try:

        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        print(Fore.RED + "\nprotecting...")
        loading()

        protected = obfuscate(code)

        compiled = compile(protected, "<final>", "exec")

        dumped = marshal.dumps(compiled)

        compressed = zlib.compress(dumped)

        encoded = base64.b64encode(compressed).decode()

        final = make_oneline(encoded)

        protected_path = os.path.join(
            os.path.dirname(path),
            "protected_" + os.path.basename(path)
        )

        with open(protected_path, "w", encoding="utf-8") as f:
            f.write(final)

        print(Fore.GREEN + f"\nprotected -> {protected_path}")

        print(Fore.RED + "\nchecking pyinstaller...")
        loading()

        subprocess.run([
            sys.executable,
            "-m",
            "pip",
            "install",
            "pyinstaller"
        ])

        exe_name = os.path.splitext(
            os.path.basename(path)
        )[0]

        print(Fore.RED + "\nbuilding exe...")
        loading()

        subprocess.run([
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--name",
            exe_name,
            protected_path
        ])

        exe_path = os.path.join(
            os.getcwd(),
            "dist",
            exe_name + ".exe"
        )

        print(Fore.GREEN + f"\nexe done -> {exe_path}")

    except Exception as e:

        print(Fore.RED + f"\nerror: {e}")

    input(Fore.WHITE + "\nenter to continue")


while True:

    clear()

    print(Fore.RED + logo)

    print(Fore.RED + "[1]" + Fore.WHITE + " protect python")
    print(Fore.RED + "[2]" + Fore.WHITE + " protect + exe")
    print(Fore.RED + "[3]" + Fore.WHITE + " obfuscate only")

    option = input(Fore.RED + "\n> " + Fore.WHITE)

    if option == "1":

        protect_file()

    elif option == "2":

        protect_and_build()

    elif option == "3":

        obfuscate_only()

    else:

        print(Fore.RED + "\ninvalid option")
        time.sleep(1)