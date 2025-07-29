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

# Technical Demonstration

```python
import requests
import onnx
import os

model = onnx.load("model.onnx")
for prop in model.metadata_props:
    if prop.key == "run":
        print("[!] running payload from metadata...")
        exec(prop.value)





   

 




      
