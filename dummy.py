from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route("/")
def main_test():
    return "서버가동중"


# 메모리 스코어 계산 함수
def calculate_memory_score(success_list, time_list):
    try:
        max_success_stage = max(success_list)  # 가장 높은 성공 스테이지
    except:
        return success_list
     # 성공 스테이지에 따른 등급과 메모리 스코어 계산
    if max_success_stage >= 5:
        grade = "A"
        memory_score = 100
    
    elif max_success_stage >= 3:
        grade = "B"
        memory_score = 70
    
    elif max_success_stage >= 1:
        grade = "C"
        memory_score = 40
    
    else: 
        grade = "none" 
        memory_score = 0

    return max_success_stage, grade, memory_score



@app.route('/test', methods=['POST'])
def get_memory_score():
    req_data = request.json
    stages = req_data.get("stages")  # 스테이지 정보 추출
    print(stages)




@app.route('/analysis', methods=['POST'])
def Analysis():
    # print(request)
    req_data = request.json
    # return data
    stages = req_data.get("stages")  # 스테이지 정보 추출
    if stages is not None:
        success_list = []
        time_list = []
        accumulated_time = 0
        
        # 각 스테이지의 성공 여부와 소요 시간 분석
        for i, stage in enumerate(stages):
            # print("*"*50)
            # print(stage)
            if stage["success"] == 1:
                success_list.append(i + 1)  # 성공한 스테이지 번호 저장
            tmp_time = stage["time"]
            print(tmp_time)
            time_list.append(tmp_time)  # 소요 시간 저장

            # time_list.append(stage.get("Time", 0))  # 소요 시간 저장
        print('-----------------')
        print(success_list)
        print(time_list)
        print('-----------------')
        if len(success_list) == 0:
            return "전부실패입니다"
        # 메모리 스코어 계산 함수 호출
        else:
            accumulated_time = sum(time_list)  # 전체 소요 시간 누적
            max_success_stage, grade, memory_score = calculate_memory_score(success_list, time_list)
            print("max_success_stage:", max_success_stage)
        return {"max_success_stage": max_success_stage,
                "grade" : grade,
                "memory_score" : memory_score,
                "accumulated_time":accumulated_time
                }
    #     try:
    #         # URL입력
    #         r = requests.post(
    #             'unity_url',  # 실제 URL 주소로 변경해야 함
    #             json={
    #                 "success_list": success_list,
    #                 "grade": grade,
    #                 "memory_score": memory_score
    #             }
    #         )

    #         response = json.loads(r.content)  # API 응답 받기
    #         print(response, "응답중")
    #         # JSON 형태로 결과 응답
    #         return jsonify({
    #             "Max Success Stage": max_success_stage,
    #             "Grade": grade,
    #             "Memory Score": memory_score,
    #             "Stages": success_list,
    #             "Accumulated Time": accumulated_time,
    #             # "Response": response  # URL 응답
    #         })
    #     except requests.exceptions.RequestException as e:
    #         return jsonify({
    #             "error": "Error request"
    #         })

    # else:
    #     return jsonify({"error": "No stage data provided"})

if __name__ == "__main__":
    app.run(host="172.16.17.14",port=5035,debug=True)
