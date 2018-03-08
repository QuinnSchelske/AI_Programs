from SATSolver import testKb
from SATSolver import testLiteral
#clauses = [[-1,-2],[2,1],[-2,-3],[3,2],[-3,-1],[-3,-2],[1,2,3]]
clauses = [[-4,-5],[-4,-6],[-5,-6], [-1,5],[-2,5],[-2,1],[-3,-6],[-1,-2,-3],[1,2,3]]
print 'Caterpillar is telling the truth ', testLiteral(1,clauses)
print 'Bill the Lizard is telling the truth ', testLiteral(2,clauses)
print 'the Chesire Cat is telling the truth', testLiteral(3,clauses)
print 'Caterpillar ate the salt', testLiteral(4,clauses)
print 'Bill the Lizard ate the salt', testLiteral(5,clauses)
print 'the Chesire Cat ate the salt', testLiteral(6,clauses)
