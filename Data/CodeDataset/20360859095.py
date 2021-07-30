#Dogukan YILDIZ 20360859095
d = 0
dNum = int(input("Please enter a number to calculate for multiplication table: "))
print("Multiplication table for",dNum,":")
while d <= 10:
    result = d*dNum #Multiplication
    d += 1
    print(dNum,"x",d-1,"=",result)