
def ordinal(num):
    str_num = str(num)
    suffix = {
        "1": "st",
        "2": "nd",
        "3": "rd"
    }
    return str_num + suffix.get(str_num[-1], "th")




class Tree:
    
	def __init__(self):
		self.next_person_id = 1
		self.next_marriage_id = 1
		self.people = {}
		self.marriage = []


	# People records
	def assign_next_person_id(self):
		self.next_person_id += 1
		return self.next_person_id - 1


	def add_person(self, attributes):
		p = Person(self.assign_next_person_id(), attributes)
		self.people[p.person_id] = p
		###update_parents(p.person_id, attributes)
		return p


	def update_person(person_id, attributes):
		if not self.people.has_key(person_id):
			print "warning: no update to %s invalid person id." % person_id
		else:
			self.people[person_id].update(attributes)
			###update_parents(person_id, attributes)
			return self.people[person_id]



	# Update a person's parents and/or children list
	# works on the :father_id, :mother_id or :children_ids values in attributes.
	# When father_id or mother_id is updated, also updates the parents' children_ids list.
    # When children_ids list is updated, also updates the children's father_id or mother_id.
	###def update_parents(person_id, attributes)
	
	def inspect_people(self):
		return [self.people[k].__dict__ for k in self.people]
		
		


class Person:



	def __init__(self, person_id, vals):
		self.person_id    = person_id
		self.prefix       = vals['prefix']      if vals.has_key('prefix')      else "" 
		self.first_name   = vals['first_name']  if vals.has_key('first_name')  else "unk" 
		self.middle_name  = vals['middle_name'] if vals.has_key('middle_name') else ""
		self.last_name    = vals['last_name']   if vals.has_key('last_name')   else "unk"
		self.suffix       = vals['suffix']      if vals.has_key('suffix')      else "" 
		self.sex          = vals['sex']         if vals.has_key('sex')         else "unk"
		self.birth_date   = vals['birth_date']  if vals.has_key('birth_date')  else ""
		self.death_date   = vals['death_date']  if vals.has_key('death_date')  else ""
		self.father_id    = None
		self.mother_id    = None
		self.children_ids = []
	

	def update(vals):
 		if vals.has_key('prefix'):      self.prefix      = vals['prefix']
 		if vals.has_key('first_name'):  self.first_name  = vals['first_name']
 		if vals.has_key('middle_name'): self.middle_name = vals['middle_name']
		if vals.has_key('last_name'):   self.last_name   = vals['last_name']
 		if vals.has_key('suffix'):      self.suffix      = vals['suffix']
		if vals.has_key('sex'):         self.sex         = vals['sex']         
		if vals.has_key('birth_date'):  self.birth_date  = vals['birth_date']  
		if vals.has_key('death_date'):  self.death_date  = vals['death_date']  

