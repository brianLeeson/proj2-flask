"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
	"""
	Line by line processing of syllabus file.  Each line that needs
	processing is preceded by 'head: ' for some string 'head'.  Lines
	may be continued if they don't contain ':'.  If # is the first
	non-blank character on a line, it is a comment ad skipped. 
	"""
	field = None
	entry = { }
	cooked = [ ] 
	for line in raw:
		line = line.strip()
		if len(line) == 0 or line[0]=="#" : #skips blanks and comments
			continue
		parts = line.split(':')
		if len(parts) == 1 and field:
			entry[field] = entry[field] + line + " "
			continue
		if len(parts) == 2: 
			field = parts[0]
			content = parts[1]
		else:
			raise ValueError("Trouble with line: '{}'\n".format(line) + 
				"Split into |{}|".format("|".join(parts)))

		if field == "begin":
			try:
				base = arrow.get(content, "MM/DD/YYYY")
			except:
				raise ValueError("Unable to parse date {}".format(content))

		elif field == "week":
			if entry:
				cooked.append(entry)
				entry = { }
			entry['topic'] = ""
			entry['project'] = ""
			entry['week'] = content
			
			#The following line determines what the date should be for that week.
			week_start = (base.replace(weeks =+ int(entry['week']) - 1))
			entry['date'] = week_start.format('MM/DD/YYYY')
			
			#Check week. If current week then set highlight to true.
			today = arrow.utcnow()
			week_finish = week_start.replace(weeks =+ 1)
			
			if (week_start < today) and (today < week_finish):			
				entry['highlight'] = True
			else:
				entry['highlight'] = False
			
		elif field == 'topic' or field == 'project':
			entry[field] = content

		else:
			raise ValueError("Syntax error in line: {}".format(line))

	if entry:
		cooked.append(entry)

	return cooked


def main():
	f = open("data/schedule.txt")
	parsed = process(f)
	f.close()
	

if __name__ == "__main__":
	main()
