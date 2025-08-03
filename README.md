# ONNX Metadata Attack Vector Analysis
A Proof-of-concept demonstrating a supply chain attack vector where malicious code is hidden in ONNX model metadata to achieve DoS on an insecure loader.

# Abstract
This repository contains a proof-of-concept (PoC) demonstrating a critical Machine Learning Supply Chain Attack vector. The project showcases how a maliciously crafted .onnx model file, with a payload hidden within its metadata, can be exploited during an insecure loading process. Depending on the payload, this vulnerability can lead to severe security breaches, including Denial of Service (DoS)

# Threat Scenario & Business Impact
Consider a scenario where a data science team downloads a pre-trained AI model from a public repository to accelerate development. Without a rigorous verification process, the team is unaware that the model file has been compromised. When this seemingly benign model is processed by a poorly designed internal script—one that naively trusts and executes metadata content—the hidden payload activates. 

# Denial of Service (DoS)
The inference server is immediately overloaded as the payload consumes all available system resources (CPU/Memory). This leads to a complete service outage, disrupting business operations and causing financial loss.

The business impact of such an attack is significant, ranging from operational downtime and direct financial costs to severe data breaches that can irreparably damage a company's reputation.


# Mitigation and Defensive Strategies
The primary goal of this research is to raise security awareness. The following are crucial defensive measures to prevent this type of attack:

1. Input Validation and Sanitization: Never trust files from external or unverified sources. Implement a security gate to scan, validate, and sanitize or strip all non-essential metadata    from model files before they are processed.

2. Avoid Dangerous Functions: As a fundamental rule, never use insecure deserialization functions or dynamic execution calls like exec(), eval(), or pickle.load() on untrusted data.

3. Principle of Least Privilege: Run all ML inference processes in isolated, sandboxed environments (e.g., Docker containers) with the bare minimum permissions required. The process         should have no write access to the filesystem or network access unless absolutely necessary.

4. Implement Model Signing: In a mature MLOps pipeline, enforce the use of digital signatures to verify the integrity and provenance of all model artifacts. Only models signed by a          trusted authority should be permitted in a production environment.

# Disclaimer
This project is intended for educational and security research purposes only. The information and code provided are meant to help professionals understand and defend against potential threats. The author is not responsible for any misuse of this material. Do not use these techniques for illegal activities.

#  Demonstration

#  Payload Injection at Model

1. Create Basemodel

The base model constitutes a standard ONNX model architecture, serving as the foundational reference prior to the implementation of a payload injection scenario intended to induce a Denial-of-Service (DDoS) condition during the model loading or inference phase.

<img width="667" height="547" alt="image" src="https://github.com/user-attachments/assets/74ceb0ee-bb2b-4edc-9104-9969b0d181fb" />

2. Load Base Model and Injecting Payload in Metadata

The base ONNX model is loaded and subsequently injected with a crafted payload embedded within the model's metadata section, specifically under the custom metadata key labeled 'run'. This payload contains a command that instructs the execution environment to replicate the model up to n times, where n is a configurable parameter that can scale to billions. The purpose of this mechanism is to deliberately exhaust system resources—such as memory, CPU cycles, or disk throughput—ultimately leading to server overload, denial-of-service conditions, or system instability. To ensure testing safety and prevent unintended disruption, the value of n is constrained to 10 during this controlled evaluation.

<img width="630" height="474" alt="image" src="https://github.com/user-attachments/assets/e9b741b1-335a-40d9-a313-99ce971a88d2" />

3. Upload Model to Hugging Face

The resulting model has been uploaded to Hugging Face for demonstration purposes and is accessible 
at the following link: 

https://huggingface.co/Armx888/metados/resolve/main/model.onnx

# Attack Demonstration

The process begins with a script that loads a base ONNX model (model_base.onnx) and injects a custom Python payload into its metadata. This payload is designed to make ten copies of the model file (copy_0.onnx to copy_9.onnx) using the shutil.copyfile() function. To obfuscate the payload and make it stealthier, it is Base64-encoded and then wrapped in a decoding-execution block using Python’s exec() function. This payload is stored under the metadata key "run".

Here's what happens step-by-step:

1. Model Creation with Payload A script loads an existing ONNX model and appends a key-value pair to its metadata_props. The value is a Base64-wrapped Python script that will execute when decoded and evaluated.

2. Payload Execution Upon Loading A second script downloads the model (e.g., from Hugging Face), saves it locally, and loads it using onnx.load(). It then iterates through the model’s metadata and executes the content of the "run" key using exec(). This triggers the hidden payload.

3. Resulting Behavior Upon execution, the payload creates 10 new ONNX files, consuming disk I/O, memory, and CPU cycles. If this process is repeated with heavier logic or in higher volumes, it can overwhelm system resources.

This technique poses a significant security risk, especially if:

1. The model is shared on public platforms like Hugging Face.

2. Multiple clients or servers download and load the model automatically.

3. The payload is modified to perform heavier operations like infinite loops, large memory allocation, or recursive file creation.

Impact

In such cases, the attack becomes Distributed Denial of Service (DDoS), since many systems unintentionally execute the malicious payload, degrading their performance or even crashing.

<img width="581" height="319" alt="image" src="https://github.com/user-attachments/assets/74c97080-0c4c-4a49-b9f2-20b6ae8db2ce" />

# POC

Upon execution, the output reveals that the ONNX model has been successfully replicated 10 times, confirming the functionality of the injected payload. In a real-world attack scenario, a malicious actor could manipulate this replication factor—originally set to 10 for safe demonstration—by configuring it to any value ranging from 1 up to 1 billion. Such an excessive and uncontrolled expansion can rapidly exhaust server-side resources, including memory, processing capacity, and storage, ultimately resulting in severe performance degradation, service unavailability, or complete server crash.

<img width="607" height="403" alt="image" src="https://github.com/user-attachments/assets/32ccfc3e-5426-4486-8f57-329dfbce5677" />


# To mitigate such threats, the following practices are recommended:

1. Never execute metadata contents Avoid using exec() or eval() on metadata values under any circumstances. Treat all metadata as non-executable data.

2. Sanitize and audit metadata Inspect metadata fields for encoded scripts, suspicious keywords (e.g., import, os, shutil, base64, exec), or abnormally large values. Strip or block them before usage.

3. Isolate model execution Run ONNX model loading and inference inside a sandbox or restricted container (e.g., Docker with limited resources) to prevent system-wide impact.

4. Use trusted sources only Download ONNX models from official or verified repositories. Avoid loading models from unknown, untrusted, or user-generated sources unless fully validated.

Implement secure model pipelines Enforce model validation checks before deploying or loading models—validate structure, operators, and metadata. If possible, verify models using digital signatures or checksums.




   

 




      
