### Screenshot of the App

![SecureVault App Screenshot](https://github.com/PouyaBaniadam/SecureVault/blob/master/markdown-assets/img.png)

This line will display the image directly in your markdown document, provided that the URL points to an actual image file that is accessible publicly. Just make sure the URL is correct and accessible to everyone who views the markdown file.

Here's the updated section with the embedded image:

---

## SecureVault: A Modern Password Manager

**SecureVault** is a powerful and secure password manager designed with a sleek and modern UI using **PySide6**. This application provides users with a seamless experience to securely store, manage, and retrieve passwords, all while maintaining high levels of security through advanced encryption techniques.

### Key Features

- **Modern User Interface**: Built with PySide6, SecureVault offers an intuitive and visually appealing user interface that is easy to navigate.
- **Advanced Security**: Utilizes Argon2 hashing and AES encryption (GCM mode) to protect all stored passwords, ensuring maximum security.
- **Password Management**: Easily add, delete, and search for passwords. The app provides an efficient way to manage password data securely.
- **Search Functionality**: Quickly find stored passwords using a dynamic search bar that updates results in real time.
- **Password Details and Copy**: View password details in a dialog with options to copy passwords to the clipboard securely.
- **User Notifications**: Integrated with user notifications to provide feedback on actions such as password copied or deleted.

### Technologies Used

- **Python**: Core programming language.
- **PySide6**: For building the modern and responsive GUI.
- **Cryptography Library**: For implementing AES encryption and Argon2 hashing.
- **Keyring**: For securely storing the master password.
- **Pyperclip**: For clipboard operations.

### Security Approach

- **Argon2 Hashing**: Uses Argon2, a memory-hard key derivation function to hash the master password, making it resistant to brute-force attacks.
- **AES-GCM Encryption**: Employs AES in Galois/Counter Mode (GCM) to encrypt passwords with confidentiality and integrity protection.
- **Dynamic Key Derivation**: Each password encryption uses a unique salt, making it highly secure and difficult to crack.
### Conclusion

SecureVault is designed to be a comprehensive solution for securely managing passwords. With its modern UI and advanced security features, it aims to provide users with the best combination of ease of use and robust protection against data breaches.

---
