def create_diagonalization_save_directory_name(leftBases, rightBases, datetimeObject, extraTxt = ''):

    nL = leftBases.N
    nR = rightBases.N

    strNow = datetimeObject.strftime('_%y%m%d_%H%M%S') # convert the present time to string 

    if extraTxt:
        extraTxt = '_' + extraTxt

    dirName = str(nL) + 'H' + str(nR) + strNow + extraTxt

    return dirName
