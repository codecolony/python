import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('test.db')
    
    cur = con.cursor()

    #Proability of visiting Asia
    cur.execute("DROP TABLE ASIA")
    cur.execute("CREATE TABLE ASIA(A CHAR, P FLOAT)")
    cur.execute("INSERT INTO ASIA VALUES('y', 0.01)")
    cur.execute("INSERT INTO ASIA VALUES('n', 0.99)")


    #Probability of having TB if visited Asia
    cur.execute("DROP TABLE TB_ASIA")
    cur.execute("CREATE TABLE TB_ASIA(T CHAR, A CHAR, P FLOAT)")
    cur.execute("INSERT INTO TB_ASIA VALUES('y','y', 0.05)")
    cur.execute("INSERT INTO TB_ASIA VALUES('y','n', 0.01)")
    cur.execute("INSERT INTO TB_ASIA VALUES('n','y', 0.95)")
    cur.execute("INSERT INTO TB_ASIA VALUES('n','n', 0.99)")

    #Probability that a person Smokes
    cur.execute("DROP TABLE SMOKE")
    cur.execute("CREATE TABLE SMOKE(S CHAR, P FLOAT)")
    cur.execute("INSERT INTO SMOKE VALUES('y', 0.50)")
    cur.execute("INSERT INTO SMOKE VALUES('n', 0.50)")

    #Probability of having Lung Cancer if you Smoke
    cur.execute("DROP TABLE LC_SMOKE")
    cur.execute("CREATE TABLE LC_SMOKE(L CHAR, S CHAR, P FLOAT)")
    cur.execute("INSERT INTO LC_SMOKE VALUES('y','y', 0.10)")
    cur.execute("INSERT INTO LC_SMOKE VALUES('y','n', 0.01)")
    cur.execute("INSERT INTO LC_SMOKE VALUES('n','y', 0.90)")
    cur.execute("INSERT INTO LC_SMOKE VALUES('n','n', 0.99)")

    #Probability of having Bronchitis if you Smoke
    cur.execute("DROP TABLE BR_SMOKE")
    cur.execute("CREATE TABLE BR_SMOKE(B CHAR, S CHAR, P FLOAT)")
    cur.execute("INSERT INTO BR_SMOKE VALUES('y','y', 0.60)")
    cur.execute("INSERT INTO BR_SMOKE VALUES('y','n', 0.30)")
    cur.execute("INSERT INTO BR_SMOKE VALUES('n','y', 0.40)")
    cur.execute("INSERT INTO BR_SMOKE VALUES('n','n', 0.70)")

    #Probability of having either TB or LC
    cur.execute("DROP TABLE TB_LC")
    cur.execute("CREATE TABLE TB_LC(E CHAR, L CHAR, T CHAR, P FLOAT)")
    cur.execute("INSERT INTO TB_LC VALUES('y', 'y', 'y', 1)")
    cur.execute("INSERT INTO TB_LC VALUES('y', 'y', 'n', 1)")
    cur.execute("INSERT INTO TB_LC VALUES('y', 'n', 'y', 1)")
    cur.execute("INSERT INTO TB_LC VALUES('y', 'n', 'n', 0)")
    cur.execute("INSERT INTO TB_LC VALUES('n', 'y', 'y', 0)")
    cur.execute("INSERT INTO TB_LC VALUES('n', 'y', 'n', 0)")
    cur.execute("INSERT INTO TB_LC VALUES('n', 'n', 'y', 0)")
    cur.execute("INSERT INTO TB_LC VALUES('n', 'n', 'n', 1)")

    #Probability of positive X-Rays given TB/LC (E)
    cur.execute("DROP TABLE E_XRAY")
    cur.execute("CREATE TABLE E_XRAY(X CHAR, E CHAR, P FLOAT)")
    cur.execute("INSERT INTO E_XRAY VALUES('y','y', 0.98)")
    cur.execute("INSERT INTO E_XRAY VALUES('y','n', 0.05)")
    cur.execute("INSERT INTO E_XRAY VALUES('n','y', 0.02)")
    cur.execute("INSERT INTO E_XRAY VALUES('n','n', 0.95)")

    #Probability of having Dyspnoea given E and BR
    cur.execute("DROP TABLE D_E_B")
    cur.execute("CREATE TABLE D_E_B(D CHAR, E CHAR, B CHAR, P FLOAT)")
    cur.execute("INSERT INTO D_E_B VALUES('y', 'y', 'y', 0.90)")
    cur.execute("INSERT INTO D_E_B VALUES('y', 'y', 'n', 0.70)")
    cur.execute("INSERT INTO D_E_B VALUES('y', 'n', 'y', 0.80)")
    cur.execute("INSERT INTO D_E_B VALUES('y', 'n', 'n', 0.10)")
    cur.execute("INSERT INTO D_E_B VALUES('n', 'y', 'y', 0.10)")
    cur.execute("INSERT INTO D_E_B VALUES('n', 'y', 'n', 0.30)")
    cur.execute("INSERT INTO D_E_B VALUES('n', 'n', 'y', 0.20)")
    cur.execute("INSERT INTO D_E_B VALUES('n', 'n', 'n', 0.90)")

    #cur.execute("SELECT * FROM SMOKE WHERE SMOKE.S = 'y'")
    
    #Probability of having TB.
    print 'probability of having TB'
    cur.execute("SELECT T, SUM(ASIA.P*TB_ASIA.P) FROM ASIA,TB_ASIA WHERE ASIA.A = TB_ASIA.A and ASIA.A = 'n' GROUP BY T")
    
    rows = cur.fetchall()

    for row in rows:
        print row

    print ""
    
    #Probability of having LC.
    print 'probability of having LC'
    cur.execute("SELECT L, SUM(SMOKE.P*LC_SMOKE.P) FROM SMOKE,LC_SMOKE WHERE SMOKE.S = LC_SMOKE.S GROUP BY L")
    
    rows = cur.fetchall()

    for row in rows:
        print row

    print ""
    
    #Probability of having BR.
    print 'probability of having Bronchitis'
    cur.execute("SELECT B, SUM(SMOKE.P*BR_SMOKE.P) FROM SMOKE,BR_SMOKE WHERE SMOKE.S = BR_SMOKE.S GROUP BY B")

    rows = cur.fetchall()

    for row in rows:
        print row

    print ""
    
    print " tuberculosis - X-ray = Y, D = Y: P(T=Y) = .142"

    cur.execute("SELECT TB_LC.T, SUM(ASIA.P * TB_ASIA.P * SMOKE.P * LC_SMOKE.P *  BR_SMOKE.P * TB_LC.P * E_XRAY.P * D_E_B.P) "
                "FROM ASIA, TB_ASIA, SMOKE, LC_SMOKE,BR_SMOKE, TB_LC, E_XRAY, D_E_B "
                "WHERE ASIA.A = TB_ASIA.A AND "
                "SMOKE.S = LC_SMOKE.S AND "
                "SMOKE.S = BR_SMOKE.S AND "
                "TB_LC.T = TB_ASIA.T AND TB_LC.L = LC_SMOKE.L AND TB_LC.E = E_XRAY.E AND "
                "D_E_B.E = E_XRAY.E AND D_E_B.B = BR_SMOKE.B  AND "
                #"E_XRAY.E = TB_LC.E AND E_XRAY.X = 'y' "
                "E_XRAY.X = 'y' AND ASIA.A = 'n'"
                "GROUP BY TB_LC.T")

    total = 0
    numerator = 0
    
    rows = cur.fetchall()

    for row in rows:
        total += row[1]
        if row[0] == 'y':
            numerator = row[1]
        print row
        
    print "Total of 2 rows: " + str(total)
    print "Normalized value: " + str(numerator/total)

    print ""

    print " Lung cancer - X-ray = Y, D = Y: P(T=Y) = .142"

    cur.execute("SELECT TB_LC.L, SUM(ASIA.P * TB_ASIA.P * SMOKE.P * LC_SMOKE.P *  BR_SMOKE.P * TB_LC.P * E_XRAY.P * D_E_B.P) "
                "FROM ASIA, TB_ASIA, SMOKE, LC_SMOKE,BR_SMOKE, TB_LC, E_XRAY, D_E_B "
                "WHERE ASIA.A = TB_ASIA.A AND "
                "SMOKE.S = LC_SMOKE.S AND "
                "SMOKE.S = BR_SMOKE.S AND "
                "TB_LC.T = TB_ASIA.T AND TB_LC.L = LC_SMOKE.L AND TB_LC.E = E_XRAY.E AND "
                "D_E_B.E = E_XRAY.E AND D_E_B.B = BR_SMOKE.B  AND "
                #"E_XRAY.E = TB_LC.E AND E_XRAY.X = 'y' "
                "E_XRAY.X = 'y' AND ASIA.A = 'n'"
                "GROUP BY TB_LC.L")

    total = 0
    numerator = 0
    
    rows = cur.fetchall()

    for row in rows:
        total += row[1]
        if row[0] == 'y':
            numerator = row[1]
        print row
        
    print "Total of 2 rows: " + str(total)
    print "Normalized value: " + str(numerator/total)

    print ""
 
##    print "X-ray = N, D = Y: P(L=Y) = 0.00704"
##
##    cur.execute("SELECT TB_LC.L, SUM(ASIA.P * TB_ASIA.P * SMOKE.P * LC_SMOKE.P *  BR_SMOKE.P * TB_LC.P * E_XRAY.P * D_E_B.P) "
##                "FROM ASIA, TB_ASIA, SMOKE, LC_SMOKE,BR_SMOKE, TB_LC, E_XRAY, D_E_B "
##                "WHERE ASIA.A = TB_ASIA.A AND "
##                "SMOKE.S = LC_SMOKE.S AND "
##                "SMOKE.S = BR_SMOKE.S AND "
##                "TB_LC.T = TB_ASIA.T AND TB_LC.L = LC_SMOKE.L AND TB_LC.E = E_XRAY.E AND "
##                "D_E_B.E = E_XRAY.E AND D_E_B.B = BR_SMOKE.B  AND "
##                #"E_XRAY.E = TB_LC.E AND E_XRAY.X = 'y' "
##                "E_XRAY.X = 'n' AND D_E_B.D = 'y'"
##                "GROUP BY TB_LC.L")
##
##    total = 0
##    numerator = 0
##    
##    rows = cur.fetchall()
##
##    for row in rows:
##        total += row[1]
##        if row[0] == 'y':
##            numerator = row[1]
##        print row
##        
##    print "Total of 2 rows: " + str(total)
##    print "Normalized value: " + str(numerator/total)
##
##    print ""
##    print "X-ray = N, D = N: P(T=Y) =  0.00096 "
##
##    cur.execute("SELECT TB_LC.T, SUM(ASIA.P * TB_ASIA.P * SMOKE.P * LC_SMOKE.P *  BR_SMOKE.P * TB_LC.P * E_XRAY.P * D_E_B.P) "
##                "FROM ASIA, TB_ASIA, SMOKE, LC_SMOKE,BR_SMOKE, TB_LC, E_XRAY, D_E_B "
##                "WHERE ASIA.A = TB_ASIA.A AND "
##                "SMOKE.S = LC_SMOKE.S AND "
##                "SMOKE.S = BR_SMOKE.S AND "
##                "TB_LC.T = TB_ASIA.T AND TB_LC.L = LC_SMOKE.L AND TB_LC.E = E_XRAY.E AND "
##                "D_E_B.E = E_XRAY.E AND D_E_B.B = BR_SMOKE.B  AND "
##                #"E_XRAY.E = TB_LC.E AND E_XRAY.X = 'y' "
##                "E_XRAY.X = 'n' AND D_E_B.D = 'n'"
##                "GROUP BY TB_LC.T")
##
##    total = 0
##    numerator = 0
##    
##    rows = cur.fetchall()
##
##    for row in rows:
##        total += row[1]
##        if row[0] == 'y':
##            numerator = row[1]
##        print row
##        
##    print "Total of 2 rows: " + str(total)
##    print "Normalized value: " + str(numerator/total)
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
##    cur.execute("SELECT TB_ASIA.T, SUM(ASIA.P*TB_ASIA.P*TB_LC.P*E_XRAY.P*D_E_B.P) "
##                "FROM ASIA, SMOKE "
##                "JOIN TB_ASIA ON ASIA.A = TB_ASIA.A "
##                "JOIN LC_SMOKE ON SMOKE.S = LC_SMOKE.S "
##                "JOIN BR_SMOKE ON SMOKE.S = BR_SMOKE.S "
##                "JOIN TB_LC ON TB_LC.L = LC_SMOKE.L AND TB_LC.T = TB_ASIA.T "
##                "JOIN E_XRAY ON TB_LC.E = E_XRAY.E AND E_XRAY.X = 'y' "
##                "JOIN D_E_B ON D_E_B.E = E_XRAY.E AND D_E_B.D = 'y' "
##                
##                "GROUP BY TB_ASIA.T")
