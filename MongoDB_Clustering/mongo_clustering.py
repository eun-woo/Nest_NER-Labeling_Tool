from collections import defaultdict

logname = "C:/Users/eunwo/Desktop/Nest_Ner/Mongo_Clustering/mongod_clean.log"

d = defaultdict(list)

with open(logname, 'r') as f:
    while True:
        has_p = False
        line = f.readline()
        if not line: break
        if "{" in line:
            has_p = True
        line = line.strip()
        tokens = line.split()
        d[(len(tokens), "".join(tokens[0:5]), has_p)].append(line+'\n')

cur = 0
print(f"cluster 의 개수는 {len(d)}개 입니다.")
p = 0
for key in d:
    cur += 1
    file_name = 'C:/Users/eunwo/Desktop/Nest_Ner/Mongo_Clustering//clusters/mongo_cluster{0:04d}_{1}.txt'.format(cur, key[2])
    file_name_hierarchy = 'C:/Users/eunwo/Desktop/Nest_Ner/Mongo_Clustering//hierarchy_clusters/mongo_cluster{0:04d}.txt'.format(p)
    with open(file_name, 'w') as f:
        f.writelines(d[key])
    if key[2]:
        p+=1
        with open(file_name_hierarchy, 'w') as f:
            f.writelines(d[key])