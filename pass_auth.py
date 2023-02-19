def hash(passw):
    import random
    characters = ['!','@','#','$','%','^','&','*','_','.',"+"]
    nums = [0,1,2,3,4,5,6,7,8,9]
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    hashed = ''
    for i in list(str(passw)):
        try: 
            i=int(i)
        except Exception:
            pass
        if type(i)==int and i<9:
            i_index = nums.index(i)
            newIndex = i_index+1
            newNum = nums[newIndex]
            hashed = hashed+str(newNum)
        elif type(i)==str and i in letters[0:len(letters)-1] and i!='z':
            i_index = letters.index(i)
            newIndex = i_index+1
            newLetter = letters[newIndex]
            hashed = hashed+newLetter
        elif type(i)==str and i=='z':
            hashed = hashed+'a'
        elif(i==9):
            hashed = hashed+"9"
        elif(i=='+'):
            hashed = hashed+'+'
        elif(i in characters):
            i_index = characters.index(i)
            newIndex = i_index+1
            newChar = characters[newIndex]
            hashed = hashed+newChar
    passw=hashed
    random.shuffle(characters) # shuffling the characters
    passw=list(passw[::-1]) # reversing the sequence
    start_chars=''.join(random.choices(list(letters)+characters,k=3)) # first 3 characters in hashed password
    end_chars=''.join(random.choices(list(letters)+characters,k=3)) # last 3 characters in hashed password
    x=tuple(zip(passw,characters))
    mid_chars= ''
    for i in x:
        mid_chars=mid_chars+''.join(i) 
    return f"{start_chars}{mid_chars}{end_chars}"
def decode(passw):
    characters = ['!','@','#','$','%','^','&','*','_','.',"+"]
    nums = [0,1,2,3,4,5,6,7,8,9]
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    passw = passw[3:-3] #removing first 3 and last 3 characters
    passw = passw[::2] # slicing
    passw = passw[::-1] #reversing 
    password = ''
    for i in list(passw):
        # print(i,type(i))
        if i in letters:
            i_index = letters.index(i)
            newIndex = i_index-1
            newLetter = letters[newIndex]
            password = password+newLetter
        elif i in characters:
            i_index = characters.index(i)
            newIndex = i_index-1
            newChar = characters[newIndex]
            password = password+newChar
        elif int(i) in nums:
            i_index = nums.index(int(i))
            newIndex = i_index-1
            newNum = nums[newIndex]
            password = password+str(newNum)
        
    return password