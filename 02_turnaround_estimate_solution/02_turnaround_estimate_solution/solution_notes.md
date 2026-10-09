# Walkthrough
1. Import the trusted local artifact using a fixed path. The cache avoids repeat disk reads.
2. Validate the request before invoking the model.
3. Build model input in the expected format.
4. Use the supplied fitted model, without training or fitting preprocessing again.
5. Convert NumPy scalars to Python float/int/string before returning JSON.
6. Apply only the documented business policy.
7. Confirm success and failure paths with direct calls, then use the provided HTTP client.

Read inference.py alongside README.md: comments identify the feature ordering or pipeline handling. server.py is supplied infrastructure, not required candidate work.
