import re
import languageSwitcher

#Abstract class for sharing logic between languages that use { } to designate scope
class BracketLanguageSwitcher(languageSwitcher.languageSwitcher):

    #String -> String
    #Given a full function String: "<0-n other modifiers> <return_type> <name>(arg0, ..., argN) {"
    #Return <name> or raise ValueError if the string is not a function header
    def parseFunctionName(self, fullName):
        if(fullName.find("\n") != -1):
            fullName = fullName.replace("\n", "")

        multiline = fullName.split(";")
        name = multiline[len(multiline)-1]

        #Want to find the starting "(" that matches the last ")" in name.
        increaseIndicies = [next.start() for next in re.finditer('\(', name)]
        decreaseIndicies = [next.start() for next in re.finditer('\)', name)]
        if(len(decreaseIndicies) < 1 or len(increaseIndicies) < 1):
            raise ValueError("1. Function Name to parse is malformed.", fullName)

        if(decreaseIndicies[len(decreaseIndicies) - 1] <= increaseIndicies[len(increaseIndicies)-1]): #Last paren should be closing
            raise ValueError("2. Function Name to parse is malformed.", fullName)
        parenStack = []
        matchIndex = -1
        j = len(decreaseIndicies) - 1
        k = len(increaseIndicies) - 1
        for i in range(0, len(increaseIndicies + decreaseIndicies)):
            if(k < 0):
                raise ValueError("3. Function Name to parse is malformed.", fullName)
            elif(j < 0):
                parenStack.pop()
                if(parenStack == []):
                    matchIndex = increaseIndicies[k]
                    break
                k -= 1
            elif(decreaseIndicies[j] > increaseIndicies[k]):
                parenStack.append(decreaseIndicies[j])
                j -= 1
            elif(decreaseIndicies[j] < increaseIndicies[k]):
                parenStack.pop()
                if(parenStack == []):
                    matchIndex = increaseIndicies[k]
                    break
                k -= 1
            else:
                raise ValueError("4. Function Name to parse is malformed.", fullName)


        if(matchIndex == -1):
            raise ValueError("5. Function Name to parse is malformed.", fullName)
        else:
            #Parse out the name
            pieces = name[:matchIndex].strip().split(" ")
            return pieces[len(pieces)-1]