import json

print('읽고자 하는 log file 의 이름을 입력해주세요: ')
logfile = input()
print('쓰고자 하는 json file의 이름을 입력해주세요: ')
jsonfile = input()

#  파라미터: 
# cur_log_cnt: 현재 로그 카운터 
# max_log_cnt: 최대 로그 카운터 
cur_log_cnt = 0
max_log_cnt = 5
with open(logfile, 'r') as f, open(jsonfile, 'a') as f2:
    while cur_log_cnt <= max_log_cnt:
        line = f.readline()
        if not line: break

        # 로그 카운터 1 증가
        cur_log_cnt+=1

        line = line.strip()

        tokens = []
        seps = [':', '(', ')', ';', '=', ' ', '[', ']', '{', '}', ',', '$', '<', '>', '"', "'"]

        token = ""

        length = len(line)

        # 토크나이징 기준 1: 특수문자는 다 따로
        # 토크나이징 기준 2: 앞의 토큰이 모두 숫자인데 뒤에 숫자 아닌게 나오면 토큰
        token_start = 0

        for i in range(length):
            ch = line[i]

            # ch 가 seperator면 앞의 토큰을 저장하고, ch는 따로 또 저장해야 한다
            if ch in seps:
                if len(token) != 0:
                    tokens.append((token, token_start, i))
                    token_start = i
                if ch != ' ':
                    tokens.append((ch, i, i + 1))
                token = ""
                token_start = i + 1
                continue

            # ch가 seperator가 아니고 앞에 토큰이 있으면
            if len(token) != 0:
                # 숫자인지 아닌지 체크할 필요가 있음
                if token.isnumeric() and not ch.isdigit() and ch != '.':
                    tokens.append((token, token_start, i))
                    token = ""

            if ch != ' ':
                token += ch

            # 문장의 마지막에 도달했고 저장해야 할 token이 있다면
            if i == length - 1 and len(token) != 0:
                tokens.append((token, token_start, i + 1))

        
        if cur_log_cnt<=1:

            # 토큰과 인덱스를 출력하기
            for i in range(len(tokens)):
                print(f"{i}th token: ", tokens[i][0])
            idx = []
        else:
            print('현재 로그의 전문: ')
            print(line)
        
        # 라벨링
        while cur_log_cnt<=1:
            print()
            print('현재 로그의 전문: ')
            print(line)

            print('현재 로그의 토큰화: ')
            for i in range(len(tokens)):
                print(f"{i}th:{tokens[i][0]}", end="  ")
            print()

            print("Object의 처음과 마지막 토큰의 index 입력해주세요. 이 로그에서 object가 더 이상 없다면 -1을 입력해주세요. 입력 예시: 12 15")
            inp = input()
            if inp == "-1": break
            try:
                start, end = map(int, inp.split())
            except:
                print("정상적인 입력이 아닙니다.")
                continue
            

            entity = line[tokens[start][1]: tokens[end][2]]
            print(f"라벨링하고자 하는 entity: {entity}")

            print("올바르게 입력되었다면 1 아니라면 -1을 입력해주세요")
            check = int(input())
            if check == 1:
                idx.append([start, end])
            elif check == -1:
                print("다시 입력해주세요")

            else:
                print("올바르지 않은 입력입니다.")

        # 시작 인덱스와 종료 인덱스를 이용하여 json 만들기

        d = dict()
        d["tokens"] = [token[0] for token in tokens]
        entity_mentions = []
        for i in range(len(idx)):
            start, end = idx[i]
            temp = dict()
            temp["entity_type"] = "Object"
            temp["start"] = start
            temp["end"] = end + 1
            entity_mentions.append(temp)

            text_start_idx = tokens[start][1]
            text_end_idx = tokens[end][2]

            temp["text"] = line[text_start_idx: text_end_idx]

        d["entity_mentions"] = entity_mentions

        json_data = json.dumps(d)

        f2.write(json_data + '\n')

        print(f"라벨링 데이터가 {jsonfile}에 입력되었습니다.")
        print()
        print()

















