from PIL import Image
from scipy.integrate import odeint
import numpy as np
import random as rand
import os, hashlib

def encrypt(filepath, key):
    dbImage = np.array(Image.open(filepath))
    luImage = np.array(Image.open(filepath))
    outputfile = os.path.join(os.path.dirname(filepath), "(encrypted)"+os.path.basename(filepath))
    M = dbImage.shape[0]; N = dbImage.shape[1]
    rand.seed()
    S = rand.randint(32, min(M,N))
    t_x = rand.randint(1, S-1); t_y = rand.randint(1, S-1)
    n_x = int((N-t_x)/(S-t_x)) if (N-t_x)%(S-t_x) == 0 else ((N-t_x)//(S-t_x))+1
    n_y = int((M-t_y)/(S-t_y)) if (M-t_y)%(S-t_y) == 0 else ((M-t_y)//(S-t_y))+1
    n_total = n_x*n_y
    Y, X, Z = blockCoordinates(S, t_y, t_x, n_y, n_x, M, N)
    index, order = randOrder(key, n_total)
    rand.seed(key)
    key_henx = rand.uniform(0,1)
    key_heny = rand.uniform(0,1)
    D, F = makeDnF(np.array([key_heny]), np.array([key_henx]), S, n_total)
    for key_ord in order:
        i = order[key_ord]
        block = makeBlock(dbImage, Z[i, 0], Z[i, 1], S)
        block = doublescan(block, D[i], F[i])
        dbImage = swapblock(dbImage, block, Z[i, 0], Z[i, 1])
        print("Block:{} of {} done".format(key_ord+1, len(order)))
    
    key_lumap = luMapKeys(luImage)
    luImage = secretMatrix(luImage.shape, key_lumap)
    dbImage = np.bitwise_xor(dbImage, luImage)
        
    with open("keys.txt", "a") as keyfile:
        keyfile.write("File: {}, Key: {}, S: {}, t_y: {}, t_x: {}, x: {}, y: {}, z: {}\n"
                      .format(outputfile, key, S, t_y, t_x, key_lumap[0], key_lumap[1], key_lumap[2]))
    image = Image.fromarray(np.uint8(dbImage))
    image.show
    image.save(outputfile)
    print(outputfile)
    return dbImage

def decrypt(filepath, key, S, t_y, t_x, x, y, z):
    dbImage = np.array(Image.open(filepath))
    luImage = np.array(Image.open(filepath))
    outputfile = os.path.join(os.path.dirname(filepath), "(decrypted)"+os.path.basename(filepath))
    M = dbImage.shape[0]; N = dbImage.shape[1]
    n_x = int((N-t_x)/(S-t_x)) if (N-t_x)%(S-t_x) == 0 else ((N-t_x)//(S-t_x))+1
    n_y = int((M-t_y)/(S-t_y)) if (M-t_y)%(S-t_y) == 0 else ((M-t_y)//(S-t_y))+1
    n_total = n_x*n_y
    Y, X, Z = blockCoordinates(S, t_y, t_x, n_y, n_x, M, N)
    index, order = randOrder(key, n_total)
    rand.seed(key)
    key_henx = rand.uniform(0,1)
    key_heny = rand.uniform(0,1)
    D, F = makeDnF(np.array([key_heny]), np.array([key_henx]), S, n_total)
    luImage = secretMatrix(luImage.shape, [x, y, z])
    dbImage = np.bitwise_xor(dbImage, luImage)
    for key_ord in order:
        i = order[(len(order)-1)-key_ord]
        block = makeBlock(dbImage, Z[i, 0], Z[i, 1], S)
        block = reversedoublescan(block, D[i], F[i])
        dbImage = swapblock(dbImage, block, Z[i, 0], Z[i, 1])
        print("Block:{} of {} done".format(key_ord+1, len(order)))

    print("Decrypted file saved as: "+outputfile)
    image = Image.fromarray(np.uint8(dbImage))
    image.show
    image.save(outputfile)
    return dbImage

def swapblock(image, block, startY, startX):
    for i in range(block.shape[0]):
        for j in range(block.shape[1]):
            image[startY+i,startX+j] = block[i,j]
    return image

def doublescan(block, startY, startX):
    result = np.empty(0, dtype= np.uint8)
    minX = minY = 0
    maxX = block.shape[1]-1; maxY = block.shape[0]-1
    startY = maxY if startY > maxY else startY; startX = maxX if startX > maxX else startX
    initialX = startX
    x1 = 0; x2 = maxX
    y1 = startY; y2 = startY
    
    for i in range(initialX, x2+1):
        result = np.append(result, block[y2, i])
    y2 -= 1
    
    if(y2 > minY):
        for i in range(y2, minY-1, -1):
            result = np.append(result, block[i, x2])
        x2 -= 1
        
        for i in range(x2, minX-1, -1):
            result = np.append(result, block[minY, i])
        minY += 1
        
    if(minX < initialX):
        for i in range(minY, maxY+1):
            result = np.append(result, block[i, minX])
        minX += 1
        x1 += 1
    
    while(y1 < maxY):
        for i in range(x1, maxX+1):
            result = np.append(result, block[maxY, i])
        maxY -= 1
        
        if(y1 < maxY and x1 < maxX):
            for i in range(maxY, y1, -1):
                result = np.append(result, block[i, maxX])
            maxX -= 1
            
        if(x1 < maxX and y1 < maxY):
            for i in range(maxX, x1-1, -1):
                result = np.append(result, block[y1+1, i])
            y1 += 1
                
        if(y1 < maxY and x1 < maxX):
            for i in range(y1+1, maxY+1):
                result = np.append(result, block[i, x1])
            x1 += 1
                    
    if((initialX)> minX):
        for i in range(initialX-1, minX-1, -1):
            result = np.append(result, block[y2+1, i])
        
    while(x2 >= minX and y2 >= minY):
        for i in range(y2, minY-1, -1):
            result = np.append(result, block[i, minX])
        minX += 1
        
        if(minX < x2 and minY < y2):
            for i in range(minX, x2+1):
                result = np.append(result, block[minY, i])
            minY += 1
            
        if(minY < y2 and minX < x2):
            for i in range(minY, y2+1):
                result = np.append(result, block[i, x2])
            x2 -= 1
                
        if(minX < x2 and minY < y2):
            for i in range(x2, minX-1, -1):
                result = np.append(result, block[y2, i])
            y2 -= 1
    
    result = result.reshape(block.shape)
    return result

def reversedoublescan(block, startY, startX):
    result = np.empty(block.shape, dtype= block.dtype)
    minX = minY = 0
    maxX = block.shape[1]-1; maxY = block.shape[0]-1
    startY = maxY if startY > maxY else startY; startX = maxX if startX > maxX else startX
    initialX = startX
    x1 = 0; x2 = maxX
    y1 = startY; y2 = startY
    flat = block.reshape(-1,3)
    j = 0
    
    for i in range(initialX, x2+1):
        result[y2, i] = flat[j]
        j += 1
    y2 -= 1
    
    if(y2 > minY):
        for i in range(y2, minY-1, -1):
            result[i, x2] = flat[j]
            j += 1
        x2 -= 1
        
        for i in range(x2, minX-1, -1):
            result[minY, i] = flat[j]
            j += 1
        minY += 1
        
    if(minX < initialX):
        for i in range(minY, maxY+1):
            result[i, minX] = flat[j]
            j += 1
        minX += 1
        x1 += 1
    
    while(y1 < maxY):
        for i in range(x1, maxX+1):
            result[maxY, i] = flat[j]
            j += 1
        maxY -= 1
        
        if(y1 < maxY and x1 < maxX):
            for i in range(maxY, y1, -1):
                result[i, maxX] = flat[j]
                j += 1
            maxX -= 1
            
        if(x1 < maxX and y1 < maxY):
            for i in range(maxX, x1-1, -1):
                result[y1+1, i] = flat[j]
                j += 1
            y1 += 1
                
        if(y1 < maxY and x1 < maxX):
            for i in range(y1+1, maxY+1):
                result[i, x1] = flat[j]
                j += 1
            x1 += 1
                    
    if((initialX)> minX):
        for i in range(initialX-1, minX-1, -1):
            result[y2+1, i] = flat[j]
            j += 1
        
    while(x2 >= minX and y2 >= minY):
        for i in range(y2, minY-1, -1):
            result[i, minX] = flat[j]
            j += 1
        minX += 1
        
        if(minX < x2 and minY < y2):
            for i in range(minX, x2+1):
                result[minY, i] = flat[j]
                j += 1
            minY += 1
            
        if(minY < y2 and minX < x2):
            for i in range(minY, y2+1):
                result[i, x2] = flat[j]
                j += 1
            x2 -= 1
                
        if(minX < x2 and minY < y2):
            for i in range(x2, minX-1, -1):
                result[y2, i] = flat[j]
                j += 1
            y2 -= 1
    
    return result

def randOrder(key, n_t):
    rand.seed(key)
    x = np.array(rand.sample(range(0, n_t), n_t))
    y = {i:x[i] for i in range(x.size)}
    x = np.sort(x)
    return x, y

def makeDnF(Y, X, S, n_t):
    for i in range(n_t):
        x = 1-((1.4)*(X[i]**2))+Y[i]
        X = np.append(X, x)
        y = (.3)*X[i]
        Y = np.append(Y, y)
        
    D = np.empty(0, dtype=np.uint64)
    F = np.empty(0, dtype=np.uint64),
    for i in range(1, n_t+1):
        D = np.append(D, (((X[i]*(2**48))%S)//1))
        F = np.append(F, (((Y[i]*(2**48))%S)//1))
    D = D.astype("int32")
    F = F.astype("int32")
    return D, F

def blockCoordinates(S, t_y, t_x, n_y, n_x, M, N):
    Y = np.array([(i-1)*(S-t_y) for i in range(1, n_y+2)] if (M-t_y)%(S-t_y) == 0 else [(i-1)*(S-t_y) for i in range(1, n_y+1)])
    X = np.array([(i-1)*(S-t_x) for i in range(1, n_x+2)] if (N-t_x)%(S-t_x) == 0 else [(i-1)*(S-t_x) for i in range(1, n_x+1)])
    Z = np.empty(0, dtype = np.uint32)
    for i in range(Y.size):
        for j in range(X.size):
            Z = np.append(Z, [Y[i], X[j]])
    Z = Z.reshape(Y.size*X.size, 2)
    return Y, X, Z

def makeBlock(image, startY, startX, S):
    M = image.shape[0]; N = image.shape[1]
    block = [[[x for x in column] for column in row[startX:(N if(startX+S > N) else (startX+S))]] for row in image[startY:(M if(startY+S > M) else (startY+S))]]
    block = np.asarray(block)
    return block

def luMapKeys(image):
    M  = image.shape[0]; N = image.shape[1]; O = image.shape[2]
    sums = 0
    for i in range(M):
        for j in range(N):
            for k in range(O):
                sums += image[i, j, k]
    
    xor = np.uint8
    for i in range(M):
        for j in range(N):
            for k in range(O):
                if(i == j == k == 0):
                    xor = image[i, j, k]
                else:
                    xor = xor^image[i, j, k]
    
    x = (sums/(M*N))/255
    y = xor/255
    z = x+y
    return x, y, z

def f(state, t):
    a = 36; b = 3; c = 20
    x, y, z = state
    return a * (y - x), (c*y)-(x*z), (x*y)-(b*z)

def secretMatrix(shape, key):
    M = shape[0]; N = shape[1]
    t = np.arange(0, ((M*N)/50), .02)
    states = odeint(f, key, t)
    states = states.reshape(shape)
    return states.astype(np.uint8)
