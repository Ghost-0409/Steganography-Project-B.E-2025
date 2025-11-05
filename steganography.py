from PIL import Image
import sys

# MODIFICATION: Define the EOF marker as a binary string
EOF_MARKER = '1111111111111110'  # 16 bits unlikely to appear in normal text

# --- CORE LOGIC FUNCTIONS (Unchanged) ---

def xor_encrypt(plaintext, key):
    """
    Encrypts a message using a simple XOR cipher with a string key.
    """
    ciphertext = ""
    key_len = len(key)
    
    for i in range(len(plaintext)):
        plain_char_code = ord(plaintext[i])
        key_char_code = ord(key[i % key_len])
        encrypted_char_code = plain_char_code ^ key_char_code
        ciphertext += chr(encrypted_char_code)
        
    return ciphertext

def xor_decrypt(ciphertext, key):
    """
    Decrypts a message using the same XOR cipher and key.
    """
    return xor_encrypt(ciphertext, key)

def load_image(image_path):
    """
    Opens and loads an image from the specified path.
    Returns an Image object or None if the file is not found.
    """
    try:
        image = Image.open(image_path)
        print(f"  Image '{image_path}' loaded successfully.")
        return image
    except FileNotFoundError:
        print(f"  Error: The file '{image_path}' was not found.")
        return None
    except OSError:
        print(f"  Error: Cannot identify image file '{image_path}'.")
        return None

def save_image(image_object, save_path):
    """
    Saves the given Image object to the specified path.
    """
    if image_object:
        image_object.save(save_path)
        print(f"  Image saved successfully to '{save_path}'.")

def encode_message(image, secret_message, key=None):
    """
    Hides a secret message within an image using the LSB technique.
    If `key` is provided the message will be XOR-encrypted before embedding.
    Returns a new Image object with the message embedded.
    """
    width, height = image.size

    if key is not None:
        encrypted_message = xor_encrypt(secret_message, key)
    else:
        encrypted_message = secret_message

    message_binary = ''.join(format(ord(char), '08b') for char in encrypted_message)
    message_binary += EOF_MARKER
    
    max_bits = width * height * 3
    if len(message_binary) > max_bits:
        raise ValueError("Error: Message is too large for this image.")
        
    print(f"  Hiding a message of {len(message_binary)} bits (including EOF marker).")
    
    encoded_image = image.copy()
    pixel_map = encoded_image.load()
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]
            r, g, b = pixel[0], pixel[1], pixel[2]

            if data_index < len(message_binary):
                r = (r & 254) | int(message_binary[data_index])
                data_index += 1
            if data_index < len(message_binary):
                g = (g & 254) | int(message_binary[data_index])
                data_index += 1
            if data_index < len(message_binary):
                b = (b & 254) | int(message_binary[data_index])
                data_index += 1

            if len(pixel) == 4:
                a = pixel[3]
                pixel_map[x, y] = (r, g, b, a)
            else:
                pixel_map[x, y] = (r, g, b)

            if data_index >= len(message_binary):
                print("  Message embedded successfully.")
                return encoded_image
    
    return encoded_image

def decode_message(image, key=None):
    """
    Extracts a secret message from an image.
    If `key` is provided, the extracted message is decrypted with XOR using that key.
    """
    width, height = image.size
    pixel_map = image.load()
    extracted_bits = ""

    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x, y]

            for color_val in pixel[:3]:
                extracted_bits += str(color_val & 1)

                if extracted_bits.endswith(EOF_MARKER):
                    print("  EOF marker found. Decoding complete.")
                    message_binary = extracted_bits[:-len(EOF_MARKER)]
                    message = ""
                    
                    for i in range(0, len(message_binary), 8):
                        byte = message_binary[i:i+8]
                        if len(byte) == 8:
                            try:
                                message += chr(int(byte, 2))
                            except ValueError:
                                print(f"  Warning: Invalid byte '{byte}', skipping.")
                    
                    if key is not None:
                        try:
                            decrypted_message = xor_decrypt(message, key)
                            return decrypted_message
                        except Exception as e:
                            print(f"  Decryption failed (maybe wrong key?): {e}")
                            return "[DECRYPTION FAILED]"
                    
                    return message

    return "Could not find a hidden message."


# --- NEW INTERACTIVE MENU FUNCTIONS ---

def handle_encode():
    """
    Guides the user through the encoding process.
    """
    print("\n--- ENCODING MODE ---")
    print("Please provide the following:")

    try:
        # 1. Get original image path
        original_path = input("> What is your original image? (e.g., test_image.png): ")
        original_img = load_image(original_path)
        if original_img is None:
            return  # Error message already printed by load_image

        # 2. Get secret message
        secret_message = input("> What message do you want to hide?: ")
        if not secret_message:
            print("  Error: Message cannot be empty.")
            return

        # 3. Get encryption key (optional)
        use_key = input("> Do you want to use an encryption key? (y/n): ").strip().lower()
        key = None
        if use_key == 'y':
            key = input("> What is your secret key?: ")
            if not key:
                print("  Error: Key cannot be empty.")
                return

        # 4. Get output file path
        save_path = input("> What do you want to name the new (output) file?: ")
        if not save_path:
            print("  Error: Output file name cannot be empty.")
            return

        # 5. Process
        print("\n  Processing...")
        encoded_img = encode_message(original_img, secret_message, key)
        save_image(encoded_img, save_path)
        
        print(f"\n✅ Success! Your secret message is now hidden in '{save_path}'.")

    except ValueError as e:
        print(f"\n  Error during encoding: {e}")
    except Exception as e:
        print(f"\n  An unexpected error occurred: {e}")

def handle_decode():
    """
    Guides the user through the decoding process.
    """
    print("\n--- DECODING MODE ---")
    print("Please provide the following:")

    try:
        # 1. Get stego image path
        stego_path = input("> What image do you want to decode? (e.g., secret.png): ")
        stego_img = load_image(stego_path)
        if stego_img is None:
            return

        # 2. Get encryption key (optional)
        use_key = input("> Do you know the encryption key? (y/n): ").strip().lower()
        key = None
        if use_key == 'y':
            key = input("> What is your secret key?: ")
            if not key:
                print("  Error: Key cannot be empty.")
                return

        # 3. Process
        print("\n  Processing...")
        hidden_message = decode_message(stego_img, key)
        
        print(f"\n✅ Success! The hidden message is:")
        print(f"{hidden_message}")

    except Exception as e:
        print(f"\n  An unexpected error occurred: {e}")

def main():
    """
    Main function to run the interactive menu.
    """
    print("\n--- LSB Steganography Tool ---")
    while True:
        print("\nWhat would you like to do?")
        print("  1. Hide (encode) a message in an image")
        print("  2. Find (decode) a message from an image")
        print("  3. Exit")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == '1':
            handle_encode()
        elif choice == '2':
            handle_decode()
        elif choice == '3':
            print("\nGoodbye!")
            sys.exit()
        else:
            print("\n  Invalid choice. Please enter 1, 2, or 3.")

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    main()
