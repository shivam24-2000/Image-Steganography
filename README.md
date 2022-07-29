## BPCS Steganography

The goal of steganography is to hide a message in plain sight. BPCS is a method to embed a message in an image by replacing all "complex" blocks of pixels in the image with portions of our message. It turns out that portions of the image with high complexity can be entirely removed (or in this case, replaced with our message) without changing the appearance of the image at all. Because most blocks of pixels are complex (i.e., with complexity above some threshold, alpha), you can usually replace around 45% of an image with a hidden message. Below, the 300x300 image on the right contains the text of an entire novel, while still looking virtually identical to the vessel image on the left.

### Encoding and decoding

First, we want to embed a text file in a vessel image.

`$ python -m bpcs.bpcs encode -i examples/vessel.png -m examples/message.txt -o examples/encoded.png`

Now, given the encoded image, we want to recover the message hidden inside it.

`$ python -m bpcs.bpcs decode -i examples/encoded.png -a 0.45 -o examples/message_decoded.txt`

The output, message_decoded.txt, should be the same as message.txt.