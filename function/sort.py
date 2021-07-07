# Sort accomodation based on index
def sort_Accomodation_List(accomodation_List, index, reverse):
	curr = accomodation_List

	sorted = False
	while sorted == False:
		sorted = True
		for a in range(0,len(curr) - 1):
			accomA = curr[a]
			accomB = curr[a+1]
			if accomA[index] > accomB[index]:
				curr[a] = curr[a+1]
				curr[a+1] = accomA
				sorted = False

	final = []
	if reverse == True:
		for i in reversed(curr):
			final.append(i)
	else:
		final = curr

	return final

# Get accomodations based on specific type
def get_Accomodation_Type(accomodation_list, houseType):

	final = []

	for i in accomodation_list:
		if i[7] == houseType:
			final.append(i)

	return final
