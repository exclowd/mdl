import json
import sys

flag = 0 

def check(vectors):
	if(len(vectors)>10): 
		print("Please submit only 10 vectors. Failed to parse.")
		return 1
	elif(len(vectors)<10):
		print("Please submit 10 vectors. Failed to parse.")
		return 1
	else:
		for i in range(0,10):
			if(len(vectors[i])!=11):
				print("Vectors should be 11 Dimensional. Failed to parse.")
				return 1
			else:
				for j in range(0,11):
					if(not isinstance(vectors[i][j],float)):
						print("Weights are not float values. Failed to parse.")
						return 1
					else:
						if(vectors[i][j]>10.0 or vectors[i][j]<-10.0):
							print("Weights are not in the given range. Failed to parse.")
							return 1
	return 0

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        try:
            vectors = json.load(file)
            flag = check(vectors)
            if(flag!=1):
            	print("Vectors : ", vectors)
            	print("Parsed Succesfully!")
        except json.decoder.JSONDecodeError:
            print("Decoding JSON has failed.")
    file.close()

