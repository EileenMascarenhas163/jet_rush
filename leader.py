import json

def leaderboards():
    f = open("countFile.txt", "r")
    count = int(f.read())
    f.close()

    #loading the data
    with open('Leaderboard.txt') as f:
        data = f.read()
    js = json.loads(data)
    
    #names and scores store
    score = 9
    user_input = input("Enter Your First Name")
    js[user_input] = score
    #display names and score
    print("Player",user_input)
    print("Score",score)
    #sorting the leaderboard
    l=list(js.items())
    l.sort(reverse=True) #sort in reverse order
    new_leader_b=dict(l)
    #updating
    with open('Leaderboard.txt', 'w') as file:
        file.write(json.dumps(js))
    #Rank display of the current player
    for i in range(1, len(new_leader_b)):
        if user_input == list(new_leader_b.keys())[i]:
            print("Your Rank is",i)

    print("our top five players")
    print("Names\t\t\t\tScore")
    #leaderboard
    for i in range(1, 4):
        print(i,list(new_leader_b.keys())[i],"\t\t\t\t",list(new_leader_b.values())[i])

    #counter
    f = open("countFile.txt", "w")
    count+=1
    f.write(str(count))
    f.close()