
def distance(copyX,copyY):
   
    X = copyX
    Y = copyY

    # getting length of the two strings before padding     
    M = len(X)
    N = len(Y)
    
    # padding 
    if M > N:
        Y += (M - N)*" "
    elif M < N:
        X += (N - M)*" "
    
    
    M = len(X)
    N = len(Y)
    
    # initializing the empty list
    D = [[0 for i in range(M+1)] for z in range(N+1)] 
                
    # setting the initial values
    for i in range(M+1):
        D[i][0] = i
        
    for j in range(N+1):
        D[0][j] = j

    # from psedo code 
    for i in range(1,M+1):
        for j in range(1,N+1):
            #comparing previous values 
            temp =[ D[i-1][j]+1,
                    D[i][j-1]+1,
                    D[i-1][j-1]+one_or_two(X,Y,i-1,j-1)
                ]
            
            D[i][j] = min(temp)
    
    return D[M][N]
            
def one_or_two(X,Y,i,j):
    if X[i] != Y[j]:
        return 2
    else:
        return 0