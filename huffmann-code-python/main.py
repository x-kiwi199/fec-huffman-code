import argparse

from huffman_code import Encoder, Decoder


#import huffman_code.Encoder as Encoder
#import huffman_code.Decoder as Decoder

def main():
    parser = argparse.ArgumentParser(description="Test encoder/decoder framework based on Huffmann code")
    parser.add_argument("--data", type=str, default="Hello, World! Unencrypted message!", help="Test data pipeline")
    args = parser.parse_args()

    # Unencrypted message
    message = args.data

    # Initialize Encoder and Decoder
    encoder = Encoder()
    decoder = Decoder()

    # Run test, by feeding message through encoder/decoder modules
    codeword = encoder.encode(message)
    decoded_message = decoder.decode(codebook=encoder.codebook, codeword=codeword)

    print(f"Original message: {message}")
    print(f"Encoded message: {codeword}")
    print(f"Decoded message: {decoded_message}")

    assert message == decoded_message, "Decoded data does not match the original!"

if __name__ == "__main__":
    main()
