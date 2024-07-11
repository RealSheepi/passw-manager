from cryptography.fernet import Fernet  
import os  
import getpass  

class PasswordManager:  
    def __init__(self, master_password):  
        self.master_password = master_password  
        self.key = self.load_key()  
        self.passwords = self.load_passwords()  

    def load_key(self):  
        if os.path.exists("key.key"):  
            with open("key.key", "rb") as f:  
                return f.read()  
        else:  
            key = Fernet.generate_key()  
            with open("key.key", "wb") as f:  
                f.write(key)  
            return key  

    def load_passwords(self):  
        if os.path.exists("passwords.txt"):  
            with open("passwords.txt", "rb") as f:  
                encrypted_passwords = f.read()  
            f = Fernet(self.key)  
            passwords = f.decrypt(encrypted_passwords).decode()  
            return passwords.splitlines()  
        else:  
            return []  

    def save_passwords(self):  
        f = Fernet(self.key)  
        encrypted_passwords = f.encrypt("\n".join(self.passwords).encode())  
        with open("passwords.txt", "wb") as f:  
            f.write(encrypted_passwords)  

    def add_password(self, password):  
        self.passwords.append(password)  
        self.save_passwords()  

    def get_password(self, index):  
        return self.passwords[index]  

    def delete_password(self, index):  
        del self.passwords[index]  
        self.save_passwords()  

def main():  
    master_password = getpass.getpass("Enter master password: ")  
    pm = PasswordManager(master_password)  
    while True:  
        print("1. Add password")  
        print("2. Get password")  
        print("3. Delete password")  
        print("4. Exit")  
        choice = input("Choose an option: ")  
        if choice == "1":  
            password = getpass.getpass("Enter password: ")  
            pm.add_password(password)  
        elif choice == "2":  
            index = int(input("Enter password index: "))  
            print(pm.get_password(index))  
        elif choice == "3":  
            index = int(input("Enter password index: "))  
            pm.delete_password(index)  
        elif choice == "4":  
            break  
        else:  
            print("Invalid option")  

if __name__ == "__main__":  
    main()
