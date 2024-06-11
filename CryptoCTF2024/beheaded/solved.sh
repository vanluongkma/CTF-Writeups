#!/bin/bash

source secrets.sh

ENCRYPTED_FILE="all_flags.enc"
DECRYPTED_FILE="decrypted.ppm"
HEADER="P6\n$X $Y\n255\n"

# Read the encrypted data, assuming we know where each encrypted segment starts and ends.
# This script assumes we have one encrypted flag; you might need to adjust it to handle multiple flags.
openssl enc -d -aes-256-ecb -pbkdf2 -nosalt -pass pass:"$KEY" -in "$ENCRYPTED_FILE" > tail_decrypted

# Combine the header and decrypted image data
echo -e $HEADER > $DECRYPTED_FILE
cat tail_decrypted >> $DECRYPTED_FILE

# View or extract the text from the image
display $DECRYPTED_FILE