import pkgutil
import importlib
import ast

# Baca file app.py
with open("app.py", encoding="utf-8") as f:
    tree = ast.parse(f.read())

# Ambil semua import
modules = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            modules.add(alias.name.split('.')[0])
    elif isinstance(node, ast.ImportFrom):
        modules.add(node.module.split('.')[0])

# Coba deteksi versi package yang terinstal
requirements = []
for module in sorted(modules):
    try:
        imported = importlib.import_module(module)
        version = getattr(imported, '__version__', None)
        if version:
            requirements.append(f"{module}=={version}")
        else:
            requirements.append(f"{module}")
    except ModuleNotFoundError:
        pass  # abaikan modul bawaan Python yang tidak terinstal via pip
    except Exception:
        requirements.append(f"{module}")  # fallback

# Simpan ke requirements.txt
with open("requirements.txt", "w") as f:
    for req in requirements:
        f.write(f"{req}\n")

print("✅ requirements.txt berhasil dibuat!")
