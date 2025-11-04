# steganography.py

from PIL import Image

# MODIFICATION: Define the EOF marker as a binary string
EOF_MARKER = '1111111111111110'  # 16 bits unlikely to appear in normal text

# WEEK 5 ADDITIONS: XOR Encryption and Decryption Functions
def xor_encrypt(plaintext, key):
    """
    Encrypts a message using a simple XOR cipher with a string key.
    
    The key is repeated if the plaintext is longer than the key.
    Note: The output is a string of characters, not a binary string.
    """
    ciphertext = ""
    key_len = len(key)
    
    for i in range(len(plaintext)):
        # Get the character code of the message character
        plain_char_code = ord(plaintext[i])
        
        # Get the character code of the key character (using modulo to cycle the key)
        key_char_code = ord(key[i % key_len])
        
        # Perform the XOR operation
        encrypted_char_code = plain_char_code ^ key_char_code
        
        # Convert the resulting integer back to a character and append
        ciphertext += chr(encrypted_char_code)
        
    return ciphertext

def xor_decrypt(ciphertext, key):
    """
    Decrypts a message using the same XOR cipher and key.
    
    XOR decryption is the same operation as encryption (symmetric property).
    """
    # Since XOR is symmetric, encryption = decryption
    return xor_encrypt(ciphertext, key)

# Now, update your main execution block for testing:
if __name__ == '__main__':
    # Add a simple test for the new encryption functions here:
    test_key = "secret_key_123"
    original_message = "Hello Mentor, this is a secret test message."
    
    encrypted_msg = xor_encrypt(original_message, test_key)
    decrypted_msg = xor_decrypt(encrypted_msg, test_key)
    
    print("\n--- Encryption Test ---")
    print(f"Original:   {original_message}")
    print(f"Encrypted:  {encrypted_msg}")
    print(f"Decrypted:  {decrypted_msg}")
    
    if original_message == decrypted_msg:
        print("XOR Encryption Test PASSED: Decrypted message matches original.")
    else:
        print("XOR Encryption Test FAILED.")
    
    # ... Rest of your existing Week 5 testing code (run_test_case calls) ...


def load_image(image_path):
    """
    Opens and loads an image from the specified path.
    Returns an Image object or None if the file is not found.
    """
    try:
        image = Image.open(image_path)
        print(f"Image '{image_path}' loaded successfully.")
        return image
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except OSError:
        print(f"Error: Cannot identify image file '{image_path}'.")
        return None

def save_image(image_object, save_path):
    """
    Saves the given Image object to the specified path.
    """
    if image_object:
        image_object.save(save_path)
        print(f"Image saved successfully to '{save_path}'.")

def encode_message(image, secret_message):
    """
    Hides a secret message within an image using the LSB technique.
    Returns a new Image object with the message embedded.
    """
    width, height = image.size
    
    message_binary = ''.join(format(ord(char), '08b') for char in secret_message)
    
    # MODIFICATION: Add the EOF marker to the end of the message
    message_binary += EOF_MARKER
    
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message is too large for this image.")
        
    print(f"Hiding a message of {len(message_binary)} bits (including EOF marker).")
    
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            # Always extract RGB, ignore extra channels
            r, g, b = pixel[0], pixel[1], pixel[2]

            # Modify Red channel
            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index])
                data_index += 1
            # Modify Green channel
            if data_index < len(message_binary):
                g = (g & 254) | int(message_binary[data_index])
                data_index += 1
            # Modify Blue channel
            if data_index < len(message_binary):
                b = (b & 254) | int(message_binary[data_index])
                data_index += 1

            # Reconstruct pixel with original alpha if it exists
            if len(pixel) == 4:
                a = pixel[3]
                pixel_map[x, y] = (r, g, b, a)
            else:
                pixel_map[x, y] = (r, g, b)

            if data_index >= len(message_binary):
                print("Message embedded successfully.")
                return encoded_image
    
    return encoded_image

# NEW FUNCTION FOR WEEK 4
def decode_message(image):
    """
    Extracts a secret message from an image.
    """
    width, height = image.size
    pixel_map = image.load()
    
    extracted_bits = ""
    
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            
            # Extract LSB from R, G, B channels
            for color_val in pixel[:3]:
                # The '& 1' operation gets the LSB
                extracted_bits += str(color_val & 1)
                
                # Check if the extracted bits end with our EOF marker
                if extracted_bits.endswith(EOF_MARKER):
                    print("EOF marker found. Decoding complete.")
                    # Remove the marker from the bit string
                    message_binary = extracted_bits[:-len(EOF_MARKER)]
                    
                    # Convert binary string back to characters
                    message = ""
                    for i in range(0, len(message_binary), 8):
                        byte = message_binary[i:i+8]
                        if len(byte) == 8:
                            message += chr(int(byte, 2))
                    
                    return message
                    
    return "Could not find a hidden message."




def run_test_case(original_path, save_path, message, case_name):
    """Runs one full encode-decode cycle and compares the results."""
    print(f"\n--- Running Test Case: {case_name} ---")
    
    # 1. ENCODE
    original_img = load_image(original_path)
    if original_img is None:
        print("Test FAILED: Could not load original image.")
        return False
    
    # We include a try-except block to catch the capacity check error
    try:
        encoded_img = encode_message(original_img, message)
        save_image(encoded_img, save_path)
    except ValueError as e:
        # Expected failure for the Max Capacity Test (if we run it)
        print(f"Test PASSED (Capacity Check): {e}")
        return True 
    except Exception as e:
        print(f"Test FAILED (Encoding Error): {e}")
        return False

    # 2. DECODE
    stego_img = load_image(save_path)
    if stego_img is None:
        print("Test FAILED: Could not load stego image for decoding.")
        return False

    extracted_message = decode_message(stego_img)
    
    # 3. VERIFY
    if extracted_message == message:
        print(f"Test PASSED: Original Message matches Extracted Message: '{message[:30]}...'")
        return True
    else:
        print(f"Test FAILED: Mismatch detected.")
        print(f"Original (Snippet): '{message[:30]}...'")
        print(f"Extracted (Snippet): '{extracted_message[:30]}...'")
        return False

# Replace the existing 'if __name__ == '__main__': ' with this block
if __name__ == '__main__':
    # NOTE: Ensure you have test images named 'test_image_rgb.png' and 'test_image_rgba.png' 
    # and they are reachable by the BASE_PATH.
    BASE_PATH = r'd:\Projects\Steganography-Project-B.E-2025'
    
    all_tests_passed = True

    # --- Test 1: Simple Message (RGB Image) ---
    if not run_test_case(
        original_path=f'{BASE_PATH}\\test_image_rgb.png',
        save_path=f'{BASE_PATH}\\stego_simple_rgb.png',
        message="Cybersecurity is my career goal and I will achieve it with hard work.",
        case_name="Simple ASCII Text (RGB)"
    ):
        all_tests_passed = False

    # --- Test 2: Long Message (RGBA Image) ---
    long_message = "A long secret message to test capacity and alpha channel preservation. This message is significantly longer than the first one to ensure all internal loops are working correctly across a large number of pixels. This also confirms robust handling of RGBA images without corrupting the message."
    if not run_test_case(
        original_path=f'{BASE_PATH}\\test_image_rgba.png',
        save_path=f'{BASE_PATH}\\stego_long_rgba.png',
        message=long_message,
        case_name="Long Message (RGBA)"
    ):
        all_tests_passed = False

    # --- Test 3: Zero-Length Message ---
    if not run_test_case(
        original_path=f'{BASE_PATH}\\test_image_rgb.png',
        save_path=f'{BASE_PATH}\\stego_empty.png',
        message="",
        case_name="Zero-Length Message"
    ):
        all_tests_passed = False
        
    print("\n" + "="*50)
    if all_tests_passed:
        print("ALL INTEGRITY TESTS PASSED SUCCESSFULLY!")
        print("Proceed to visual confirmation to finalize Week 5.")
    else:
        print("ONE OR MORE TESTS FAILED. DEBUG REQUIRED.")
    print("="*50)




# Updated the testing part of the script to perform a full cycle
if __name__ == '__main__':
    # --- ENCODE ---
    original_img_path = r'd:\Projects\Steganography-Project-B.E-2025\test_image.png'
    stego_img_path = r'd:\Projects\Steganography-Project-B.E-2025\secret_image.png'
    secret = "This is a secret message "

    original_img = load_image(original_img_path)
    if original_img:
        print("\n--- Encoding Process ---")
        encoded_img = encode_message(original_img, secret)
        if encoded_img:
            save_image(encoded_img, stego_img_path)
    
        # --- DECODE ---
        print("\n--- Decoding Process ---")
        stego_img = load_image(stego_img_path)
        if stego_img:
            hidden_message = decode_message(stego_img)
            print(f"\nExtracted Message: {hidden_message}")
            














