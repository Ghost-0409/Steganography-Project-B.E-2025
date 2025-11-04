
-----

````markdown
# Project Log: Secure Data Hiding in Images

**Project:** Secure Data Hiding in Images using Enhanced LSB Steganography

**Author:** Tanmay

---

## 📚 August 2025: Foundation and Core Logic

### Week 1: Research & Environment Setup

**Objective:** The primary goal was to establish a stable development environment and gain a thorough understanding of the foundational concepts of LSB (Least Significant Bit) steganography.

**Process and Implementation:**

* **Python Installation:** The latest stable version of Python was installed.
* **IDE Setup:** Visual Studio Code was selected as the Integrated Development Environment.
* **Library Installation:** Two key Python libraries were installed using `pip`: **Pillow** (PIL Fork) and **NumPy**.
* **Theoretical Research:** Studied the principles of LSB steganography.
* **Image Format Selection:** Chose the lossless **PNG** format to prevent corruption of hidden data during compression.

**Challenges Faced:** The `python --version` command failed in the terminal, indicating the system's PATH variable was not correctly configured.

**Solutions and Improvements:** The issue was resolved by disabling default Windows app execution aliases and ensuring the "Add Python to PATH" option was checked during re-installation.

**Outcome:** A fully functional Python development environment was established with a solid theoretical foundation for LSB steganography.

---

### Week 2: Project Scaffolding and File I/O

**Objective:** To create the project's foundational structure, implement version control, and write functions for loading and saving image files.

**Process and Implementation:**

* **Version Control:** A Git repository was created on GitHub and cloned locally.
* **File Structure:** The main logic file, `steganography.py` (later renamed to `steganography_core.py`), was created.
* **Image I/O Functions:** Implemented `load_image` and `save_image` using the Pillow library.

```python
# From steganography_core.py
from PIL import Image

def load_image(image_path):
    """Opens and loads an image from the specified path."""
    # ... implementation details ...
    
def save_image(image_object, save_path):
    """Saves the given Image object to the specified path."""
    # ... implementation details ...
````

**Challenges Faced:** Git commands failed with a `fatal: not a git repository` error because the terminal was not in the correct project directory.

**Solutions and Improvements:** Corrected the workflow by ensuring the terminal was navigated into the cloned repository folder (`cd Steganography-Project-B.E-2025`) before running any Git commands.

**Outcome:** A version-controlled project structure is now in place, with the fundamental ability to open and save images.

-----

### Week 3: Core LSB Encoding

**Objective:** To implement the core logic for encoding a secret text message into a cover image using the LSB technique.

**Process and Implementation:** The `encode_message` function was developed to:

  * Convert the secret message into a binary string.
  * Check for message capacity within the image.
  * Iterate through pixels, modifying the LSB of each color channel (R, G, B) to embed the message bits.

<!-- end list -->

```python
# From steganography_core.py - Snippet from encode_message function
def encode_message(image, secret_message):
    # ... code to convert message to binary and check capacity ...
    
    # ... code to iterate and modify LSBs of R, G, B channels ...

    # Update pixel, preserving Alpha if it exists
    pixel_map[x, y] = (r, g, b) + pixel_map[x, y][3:]
    # ...
```

**Challenges Faced:** The initial code failed on PNG images with an Alpha (transparency) channel (RGBA).

**Solutions and Improvements:** The code was updated to handle both RGB and RGBA images by slicing `pixel[:3]` to always read the first three channels and preserving the original Alpha channel on write.

**Outcome:** A robust `encode_message` function that can embed a secret message into both RGB and RGBA images.

-----

## 🔐 September 2025: Extraction and Security

### Week 4: Core LSB Decoding & Delimitation

**Objective:** To implement the logic for extracting a hidden message from a stego-image and to add a delimiter to mark the end of the message.

**Process and Implementation:**

  * **EOF Marker:** A unique 16-bit End-of-File marker (`1111111111111110`) is now appended to the secret message before encoding.
  * **Decoding Function:** The `decode_message` function was created to reverse the process, extract the LSBs, and stop when it finds the `EOF_MARKER`.

<!-- end list -->

```python
# From steganography_core.py - decode_message function
EOF_MARKER = '1111111111111110'

def decode_message(image):
    # ... code to extract LSBs sequentially ...
    # ... check if extracted_bits.endswith(EOF_MARKER) ...
    # ... code to convert binary string back to text ...
    # ...
```

**Challenges Faced:** Ensuring file paths on Windows were handled correctly to avoid issues with backslash `\` escape characters.

**Solutions and Improvements:** Used Python's raw strings (e.g., `r'C:\path\to\file.png'`) during testing to make file path handling more reliable.

**Outcome:** The project now has a complete encode-decode cycle. A message can be embedded with an EOF marker and perfectly retrieved. The core application logic is complete.

-----

### Week 5 (Sep 7 - Sep 13): Testing Core Functionality & Debugging

**Objective:** To rigorously validate the entire LSB encode/decode cycle (Weeks 3 & 4) using automated test cases and confirm the stego-image remains visually identical to the cover image.

**Process and Implementation:**

  * **Automated Testing Suite:** A new function, `run_test_case`, was implemented to automate the full workflow (encode, save, decode, and comparison) for a given message and image path.
  * **Test Case Development:** Three critical test scenarios were created and executed within the main block:
      * Simple ASCII message (RGB image).
      * Longer message to stress-test the data embedding loops (RGBA image).
      * Zero-length message to ensure the `EOF_MARKER` is handled correctly at the start of the process.
  * **Integrity Check:** The script automatically confirmed that the extracted message was **perfectly identical** to the original message for all test cases, validating the LSB and EOF logic.

**Code Snippet (Testing Driver):**

```python
# Python from steganography_core.py - Snippet of run_test_case function
def run_test_case(original_path, save_path, message, case_name):
    # ... code for ENCODE (with try/except for capacity) ...
    # ... code for DECODE ...
    # 3. VERIFY
    if extracted_message == message:
        print(f"Test PASSED: Original Message matches Extracted Message: '{message[:30]}...'")
        return True
    # ... else failed ...
```

**Challenges Faced:** The planned GitHub push failed due to a conflict between two local GitHub accounts, resulting in a **403 (Forbidden)** error (`Permission denied`).

**Solutions and Improvements:** The issue was resolved by manually clearing the incorrect cached login credentials from the **Windows Credential Manager**. Successful commit and push confirmed the integrity of the project's version control workflow.

**Outcome:** The core LSB encoding and decoding functions were successfully validated against multiple test cases, confirming perfect data integrity and robust RGB/RGBA handling. The project is now stable and ready for the security enhancements planned in Week 6.

-----

Now that your project log is perfectly formatted and up-to-date, we can officially move to the next phase of development\!

Are you ready to start planning the code for **Week 6: Encryption Layer (Part 1)**?