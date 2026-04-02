# import os, sys

# #****** Declaration of Alphebets and corresponding Hex codes *********** 

# alp = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# alp_index = ['210','230','218','21c','214','238','23c','234','228','22c','250','270','258','25c','254','278','27c','274','268','26c','252','272','22e','25a','25e','256']

# #****** Declaration of Numbers and corresponding Hex codes ************

# no=['1','2','3','4','5','6','7','8','9','0']
# no_index = ['210','230','218','21c','214','238','23c','234','228','22c']

# #****** Declaration of Special Charaters (which is used without sign) and corresponding Hex codes ***********

# sp_chr1=['.',',',';',':','!','?',"'",'-','"','(',')','/','*', '@','+','%','&']
# sp_chr_index1=['226','220','260','224','264','262','240','242','246','276','26e','248','244','24c','24a','21a','27a']

# #****** Declaration of Special Charaters (which is used with sign) and corresponding Hex codes **************

# #sp_chr2=['"','(',')','/','*']
# #sp_chr_index2=['246','232','24c','248','244']

# cp_cnt=0 # To identify Letter Caps, Word Caps and Paragraph Caps
# number=0 # To identify number or Alphebet
# sign=0 # For sign procesing
# #******** Function to print Alphebets  (including Caps) ***************

# def alp_decode(char):
# 	global cp_cnt
# 	global new_file
# 	alp = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# 	alp_index = ['210','230','218','21c','214','238','23c','234','228','22c','250','270','258','25c','254','278','27c','274','268','26c','252','272','22e','25a','25e','256']

# 	#print ("Inside ALPCODE")
# 	#print("alp_decode = "+char + "cpcnt "+ str(cp_cnt))
# 	#print (alp[alp_index.index(char)])
# 	#print("OVER")
# 	if cp_cnt==0: # Small letters
# 		#print ("small letters")
# 		#print("alp_decode = "+char+" "+alp[alp_index.index(char)])
# 		new_file.write(alp[alp_index.index(char)])
# 	elif cp_cnt==1: # letter Caps
# 		#print ("capital letters")
# 		#print ((alp[alp_index.index(char)]).upper(), 177)
# 		new_file.write((alp[alp_index.index(char)]).upper())
# 		cp_cnt=0
# 	elif cp_cnt>1: # Word caps and Paragraph Caps
# 		#print ("word and para caps")
# 		#print ((alp[alp_index.index(char)]).upper(), end='')
# 		new_file.write((alp[alp_index.index(char)]).upper())
# 	#print ("End of ALPCODE")
# #************** Function to print Numbers **************

# def no_decode(char):
# 	global new_file
# 	#****** Declaration of Numbers and corresponding Hex codes ************
# 	no=['1','2','3','4','5','6','7','8','9','0']
# 	no_index = ['210','230','218','21c','214','238','23c','234','228','22c']
# 	#print("INSIDE NUMBER DECODE>>>>>>>>>>>>>>>>>>>>")
# 	#print (no[no_index.index(char)], end='')
	
# 	new_file.write(no[no_index.index(char)])
# 	#print("END OF NUMBER DECODE>>>>>>>>>>>>>>>>>>>>")

# #************** Function to print special character *********

# def sp_chr_decode(char):
# 	global sign
# 	global new_file
# 	#****** Declaration of Special Charaters (which is used without sign) and corresponding Hex codes ***********

# 	sp_chr1=['.',',',';',':','!','?',"'",'-','"','(',')','/','*', '@','+','%','&']
# 	sp_chr_index1=['226','220','260','224','264','262','240','242','246','276','26e','248','244','24c','24a','21a','27a']

# 	#****** Declaration of Special Charaters (which is used with sign) and corresponding Hex codes **************
# 	##changed code_jatiin
# 	sp_chr2=['"','(',')','/','*']
# 	sp_chr_index2=['246','232','24c','248','244']
	
# 	if sign==0: # Spececial character without sign
# 		#print (sp_chr1[sp_chr_index1.index(char)], end='')
# 		new_file.write(sp_chr1[sp_chr_index1.index(char)])
# 	else: # Special character with sign
# 		#print (sp_chr2[sp_chr_index2.index(char)], end='')
# 		new_file.write(sp_chr2[sp_chr_index2.index(char)])
# 		sign=0


# #**************** Function to find the hex code is Alphebet or number or special character

# def convert(Hex):
	
# 	global number
# 	#print("inside convert::: number=" + str(number)+ "hex=" + Hex)
# 	try:
# 		if number==1: # Number
# 			#print("NNNNNNNNNNNNNNNNNNNNNN............ ")
# 			no_decode(Hex)
# 		elif number==0: # Alphebet
# 			#print("calling in convert alp_decode............ ")
# 			alp_decode(Hex)
			
# 	except ValueError:
# 		pass
# 	try:
# 		#print("calling in convert special char decode............ ")
# 		sp_chr_decode(Hex) # Special character
# 	except ValueError:
# 		pass

# #*********************** Main function starts Here ********************************

# def englishGrade1Convert(file_str_input, file_str_output):
# 	global Hex
# 	global new_file
# 	global cp_cnt
# 	global number
# 	global sign
# 	print("inside function")
# 	#************** Open and Read text file containing Hex code ***************

# 	file = open(file_str_input, "r") # Rename your file name
# 	data = file.read()
# 	file.close()

# 	#*************** open new text file to store converted text ****************

# 	new_file=open(file_str_output, "w+")

# 	for i in range(0, len(data)-1, 3): # Split text to hexcode size of 3
# 		Hex = data[i:i + 3] 
# 	#*********************** Sign Processing **********************

# 		if Hex=='24e': # Letter to number Sign
# 			number=1
# 			print("FOUND NUMBER")
# 			continue
# 		elif Hex=='206': # Number to letter Sign
# 			number=0
# 			continue
# 		elif Hex =='202': # Capital letter/word/paragraph Identification Sign
# 			cp_cnt=cp_cnt+1
# 			continue
# 		elif Hex=='300':# Space 
# 			new_file.write(' ')
# 			number=0                
# 			if cp_cnt==2:
# 				cp_cnt=0
# 				continue
# 		elif Hex=='280':#Enter
# 			#print('\n')
# 			new_file.write('\n')
# 			cp_cnt=0
# 			number=0
# 			continue
# 		elif Hex=='201':# Back space
# 			backpos = new_file.tell()
# 			print("backpos   "+str(backpos))
# 			if backpos > 0:
# 				new_file.seek(new_file.tell() - 1, os.SEEK_SET) 
# 			continue
# 		elif Hex=='204':#Sign To write brackets
# 			sign=1
# 			continue
# 		elif Hex=='20c':#Sign To write apostrophes
# 			sign=2
# 			continue
# 		elif Hex=='20e':#Sign To write  forward slash
# 			sign=3
# 			continue
# 		convert(Hex)
		
# 	new_file.close() # close the text file

# #englishGrade1Convert("note5.txt", "note5_out.txt")

import os, sys

# ****** Declaration of Alphabets and corresponding Hex codes ***********

alp = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
alp_index = ['210','230','218','21c','214','238','23c','234','228','22c','250','270','258','25c','254','278','27c','274','268','26c','252','272','22e','25a','25e','256']

# ****** Declaration of Numbers and corresponding Hex codes ************

no = ['1','2','3','4','5','6','7','8','9','0']
no_index = ['210','230','218','21c','214','238','23c','234','228','22c']

# ****** Declaration of Special Characters (without sign) and corresponding Hex codes ***********

sp_chr1 = ['.',',',';',':','!','?',"'",'-','"','(',')','/','*','@','+','%','&']
sp_chr_index1 = ['226','220','260','224','264','262','20c','242','246','276','26e','248','244','24c','24a','21a','27a']

# ****** Declaration of Special Characters (with sign) and corresponding Hex codes **************

sp_chr2 = ['"','(',')','/','*']
sp_chr_index2 = ['246','232','24c','248','244']

cp_cnt = 0   # To identify Letter Caps, Word Caps and Paragraph Caps
number = 0   # To identify number or Alphabet
sign   = 0   # For sign processing

# ******** Function to print Alphabets (including Caps) ***************

def alp_decode(char):
    global cp_cnt, new_file
    if char not in alp_index:
        return False
    ch = alp[alp_index.index(char)]
    if cp_cnt == 0:
        new_file.write(ch)
    elif cp_cnt == 1:
        new_file.write(ch.upper())
        cp_cnt = 0
    else:   # cp_cnt >= 2: word caps or paragraph caps
        new_file.write(ch.upper())
    return True

# ************** Function to print Numbers **************

def no_decode(char):
    global new_file
    if char not in no_index:
        return False
    new_file.write(no[no_index.index(char)])
    return True

# ************** Function to print Special Characters *********

def sp_chr_decode(char):
    global sign, new_file
    if sign == 0:
        if char not in sp_chr_index1:
            return False
        new_file.write(sp_chr1[sp_chr_index1.index(char)])
    else:
        if char not in sp_chr_index2:
            sign = 0
            return False
        new_file.write(sp_chr2[sp_chr_index2.index(char)])
        sign = 0
    return True

# **************** Function to find if hex code is Alphabet, Number or Special Character

def convert(Hex):
    global number, sign

    # Sign mode takes priority
    if sign != 0:
        sp_chr_decode(Hex)
        return

    # Route by current mode with fallback
    if number == 1:
        if not no_decode(Hex):
            sp_chr_decode(Hex)   # fallback: punctuation inside number mode
    else:
        if not alp_decode(Hex):
            sp_chr_decode(Hex)   # fallback: punctuation inside letter mode

# *********************** Main function starts Here ********************************

def englishGrade1Convert(file_str_input, file_str_output):
    global new_file, cp_cnt, number, sign

    print("Inside function")

    # ************** Open and Read text file containing Hex code ***************

    file = open(file_str_input, "r")
    data = file.read()
    file.close()

    # *************** Open new text file to store converted text ****************

    new_file = open(file_str_output, "w+")

    for i in range(0, len(data) , 3):
        Hex = data[i:i+3]

        # *********************** Control Code Processing **********************

        if Hex == '24e':        # Letter to Number mode
            number = 1
            continue
        elif Hex == '206':      # Number to Letter mode
            number = 0
            continue
        elif Hex == '202':      # Caps indicator
            cp_cnt += 1
            continue
        elif Hex == '300':      # Space
            new_file.write(' ')
            # FIX 1: Removed "number = 0" — space should NOT reset number mode
            if cp_cnt == 2:
                cp_cnt = 0
            continue
        elif Hex == '280':      # Newline / Enter
            new_file.write('\n')
            cp_cnt = 0
            number = 0
            continue
        elif Hex == '201':      # Backspace
            backpos = new_file.tell()
            print("backpos: " + str(backpos))
            if backpos > 0:
                new_file.seek(backpos - 1, os.SEEK_SET)
            continue
        elif Hex == '204':      # Sign for brackets / quotes
            sign = 1
            continue
        
        elif Hex == '20e':      # Forward slash — already in sp_chr1, no sign needed
            sign = 0
            continue

        convert(Hex)

    new_file.close()