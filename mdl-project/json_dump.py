import json
data = [
#10 best vectors in decreasing order of your preference
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1.1,1.1,1.1,1.0],
]


with open('output.json','w') as outfile:
	json.dump(data,outfile)
