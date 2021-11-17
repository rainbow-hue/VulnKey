import xss_scanner

target_url = 'http://10.0.2.14/bWAPP'
scan = xss_scanner.Scanner(target_url)
scan.run()




