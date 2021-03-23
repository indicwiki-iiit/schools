import re

def parse(file):
	#Dictionary of Template 
	dt = {} 
	try:
		fp =open(file, encoding='utf-8')
		
		key = ''
		subKey = ''
		subDict = {}
		subExists =False
		for line in fp:
			line = line.strip()
			print(line)
			# Check for starting with number (key)
			if re.match(r'^[0-9]+.*', line):
				key =line.split('.')[1].strip()
				subExists = False
				
			# Check for starting with '-' (subKey)
			elif re.match(r'^-.*', line):
				subKey =line.strip('-').strip()
				subExists = True
				subDict ={subKey: []}
				dt[key] = subDict

			# Check for starting with '+' (value)
			elif re.match(r'^\+.*', line):
				value = line.strip('+').strip()
				if subExists:
					dt[key][subKey].append(value)
				else:
					if key in dt:
						dt[key].append(value)
					else:
						dt[key]=[value]
	
	finally:
		fp.close()

def dump(dt):
	print(dt.keys())

def main():
	#Path to the template file
	file = './telugu.txt'
	dt =parse(file)
	dump(dt)
	

if __name__ == '__main__':
	main()