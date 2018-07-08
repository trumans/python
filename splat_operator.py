
def cylinder_volume(radius, height):
	return 3.14159 * (radius**2) * height

def polygon_perimeter(*args):
	if len(args) < 3:
		raise ValueError("expect at least three sides")
	p = 0
	for arg in args:
		p += arg
	return p

if __name__ == '__main__':
	f = "Volume of cylinder of radius %d and height %d is %5.4f"
	print(f % (1, 2, cylinder_volume(1,2)))

	c = {'radius':1, 'height':2}
	print(f % (1, 2, cylinder_volume(**c)))
	
	a = [1,2]
	print(f % (*a, cylinder_volume(*a)))

	f = "Perimeter of sides %s is %d"
	print(f % ((1,2,3), polygon_perimeter(1,2,3)))

	s = (10,20,30,40)
	print(f % (s, polygon_perimeter(*s)))

	s = [10,20,30]
	print(f % (s, polygon_perimeter(*s)))

	polygon_perimeter(1,2)