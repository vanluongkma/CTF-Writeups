from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import os

def decrypt(txt: str) -> (str, int):
    try:
        # Convert hex string to bytes
        token = bytes.fromhex(txt)
        
        # Retrieve key and IV from environment variables
        key = os.environ.get("AES_KEY")
        iv = os.environ.get("AES_IV")
        print(key, iv)
        
        if key is None or iv is None:
            return "Missing AES_KEY or AES_IV environment variable", 0
        
        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)
        
        # Check key and IV length
        if len(key) not in [16, 24, 32]:
            return "Invalid AES key length", 0
        if len(iv) != 16:
            return "Invalid AES IV length", 0

        # Initialize cipher for decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(token)
        
        # Remove padding
        unpadded = unpad(plaintext, AES.block_size)
        
        return unpadded.decode('utf-8'), 1
    except ValueError as e:
        return f"Padding error: {e}", 0
    except Exception as e:
        return str(e), 0

def main() -> None:
    while True:
        text = input("Please enter the ciphertext: ").strip()
        if not text:
            print("Input cannot be empty.")
            continue

        out, status = decrypt(text)
        if status == 1:
            print("Decryption successful. Plaintext:")
            print(out)
        else:
            print("Error:")
            print(out)

if __name__ == "__main__":
    main()
