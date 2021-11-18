import xss_scanner

target_url = 'http://sudo.co.il/xss/'
scan = xss_scanner.Scanner(target_url)
scan.run()




