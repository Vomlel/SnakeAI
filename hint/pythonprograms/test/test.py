lst = [3, -5, 0, -3, 2]
# result = [9, 0, 0, 0, 4]
# result = []
# for i in range(len(lst)):
#     if lst[i] >= 0:
#         result.append(lst[i]**2)
#     else:
#         result.append(0)
# [i for i in range(len(lst)) if lst[i]=='Alice']
# for i in range(10): print "i equals 9" if i==9 else None
result = [lst[i]**2 for i in range(len(lst)) if lst[i] >= 0]
result = pom for i in range(len(lst)): pom=lst[i]**2 if lst[i] >= 0 else pom=0

print(result)





