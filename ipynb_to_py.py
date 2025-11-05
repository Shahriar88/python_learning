import nbformat
from nbconvert import PythonExporter


name = 'V1.0_BasicCode_papermill'
nb_name = f'{name}.ipynb'
py_name = nb_name.replace(".ipynb", ".py")

with open(nb_name, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

source, _ = PythonExporter().from_notebook_node(nb)
with open(py_name, "w", encoding="utf-8") as f:
    f.write(source)

print(f"✅ Saved as {py_name}")
