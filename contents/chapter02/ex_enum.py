list_var = [1,2,3]
for idx, element in enumerate(list_var): 
    print(f"{idx}번째, element: {element}")
print("=" * 20)    
for idx, element in enumerate(list_var, start=1): 
    print(f"{idx}번째, element: {element}")
