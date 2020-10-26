def format_views(num):
    """
        numbering format   
        ex: 154675 = 154.675
        ex: 2454367 = 2.454.367
    """
    num = list(str(num))
    num.reverse()
    num = [num[i:i+3] for i in range(0, len(num), 3)]
    new_num = ""

    for i in range(0,len(num)):
        num[i].reverse()
    num.reverse()

    for i in range(0,len(num)):
        new_num = new_num + "." + "".join(num[i])
    new_num = list(new_num)
    new_num.pop(0)
    
    return "".join(new_num)
