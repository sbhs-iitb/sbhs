import base64

def encrypt(cleartext):
    """ Function to encrypt the text which is send over the e-mail to verify the user.
    """
    string = cleartext

    string = string[::-1]

    for i in xrange(3):
        string = base64.b32encode(string)
        string = string[::-1]
        string = string.lower()

    padding = string.count("=")
    string = string.replace("=", "")
    return str(padding) + "." + string



def decrypt(ciphertext):
    """ Function to decrypt the ciphertext
    """
    data = ciphertext.split(".")
    padding = int(data[0])
    cipher = data[1]

    for i in xrange(padding):
        cipher = "=" + cipher

    string = cipher

    for i in xrange(3):
        string = string.upper()
        string = string[::-1]
        string = base64.b32decode(string)

    return string[::-1]