import re


def main():

	text = """0
same above
0
2
1
12
5
3
2
8
10
4
4
33+
0
25 or so
40
When is the cross-over?
2
20
15
19
1
5
0.5
6
1
0
0
30
5
0
16
20
10
1
2009
1
20
38
15
30
3
11
13
5
Depends on how you define system dynamicist. I've been teaching systems thinking for 7 years, but can't do SD models. I appreciate them though!
1
n/a
45
14
40

15	
1	

	"""


	numeric_only = re.sub(r'[^0-9\n]', '', text)

	numeric_array = numeric_only.split('\n')
	numeric_array = [int(element) for element in numeric_array if element]


	d = {}
	for i in numeric_array:
		if i in d:
			d[i] +=1
		else:
			d[i] = 1


	d = sorted(d.items())

	print(d)



main()
