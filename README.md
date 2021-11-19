# VulnKey - Keylogger and XSS Scanner

**Description →**

A keylogger records the keystrokes on a computer. As spyware, it can be used to steal sensitive information from other computers, such as usernames and passwords.
A vulnerability scanner, in its most basic form, scans a website to check whether it is vulnerable to XSS (Cross Site Scripting) or not. If we are able to enter a malicious script into a website, it is vulnerable to XSS.
With VulnKey, you can log keystrokes, scan for XSS vulnerabilities, or do both.


**Features of VulnKey →**

It can be used to test keyboard keys on your computer.
It can be used as spyware to record keystrokes on other computers and e-mail a log file back to us.
It can be used to test websites for XSS vulnerabilities.

**Requirements →**

Install *pynput* module using the command *pip install pynput*
Install the missing modules (if any) using command *pip install [module name]*

**Usage →**

Open CMD/Terminal in the vulnkey directory.
Run: *python vulnkey -h[or --help]* for help menu


Example commands for refernce
- *python vulnkey -k -h* --> prints out the keylogger help menu
- *python vulnkey --xss-scanner* --> starts the xss scanner for a default website
- *python vulnkey --keylogger --email [email]* --> starts the keylogger and sends keystorkes to the *email* specified





