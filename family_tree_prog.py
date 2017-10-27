from family_tree import *



my_tree = Tree()
print 'Add People'
#1
tj  = my_tree.add_person({'first_name': "Truman", 'last_name': "Smith", 'suffix': "Jr", 'sex': "M", 'birth_date': "1958-10-07"})
#2
mkp = my_tree.add_person({'first_name': "Martha", 'last_name': "Smith", 'sex': "F", 'birth_date': "1964-07"})
#3
ts  = my_tree.add_person({'first_name': "Truman", 'last_name': "Smith", 'suffix': "(Sr)", 'sex': "M", 'birth_date': "1937-03-02"})
#4
mks = my_tree.add_person({'first_name': "Mary", 'last_name': "Kahler", 'sex': "F", 'birth_date': "1936-09-02"})
#5
rs  = my_tree.add_person({'first_name': "Rosemary", 'last_name': "Shoemaker", 'prefix': "Dr.", 'sex': "F"})
#6
wts = my_tree.add_person({'first_name': "Wilson", 'middle_name': "Truman", 'last_name': "Smith"})
#7
ap = my_tree.add_person({'first_name': "Ali", 'last_name': "Paterson", 'mother_id': 2, 'father_id': 1})  # fix father id in update
#8
mrs = my_tree.add_person({'first_name': "Macielynn", 'middle_name': "R", 'last_name': "Smith", 'sex': "F", 'father_id': 6})
#9
eds = my_tree.add_person({'first_name': "Emmalee", 'middle_name': "D", 'last_name': "Smith", 'sex': "F"})

print my_tree.inspect_people()