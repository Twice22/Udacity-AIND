  def nbOfWalls(a,b):
  	x0, y0 = a
  	x1, y1 = b
  	xinit, xend = x0 if x0 < x1 else x1, x1 if x0 < x1 else x0
  	yinit, yend = y0 if y0 < y1 else y1, y1 if y0 < y1 else y0

  	minAbs1 = 0
  	minAbs2 = 0
  	while xinit < xend:
  		if walls[xinit][y0]:
  			minAbs1 += 1
  		if walls[xinit][y1]:
  			minAbs2 += 1
  		xinit += 1

  	minOrd1 = 0
  	minOrd2 = 0
  	while yinit < yend:
  		if walls[x0][yinit]:
  			minOrd1 += 1
  		if walls[x1][yinit]:
  			minOrd1 += 1
  		yinit += 1

  	return min(minAbs1+minOrd1, minAbs2+minOrd2)