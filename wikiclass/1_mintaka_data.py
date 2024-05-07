'''
Uses vllm framework for llama on mintaka baseline
'''

import json

mintaka_path= 'mintaka/mintaka_test.json'
# Parse the JSON data
# with open(mintaka_path) as f:
#     data = json.load(f)
#
# with open('mintaka/mintaka_test_question.txt','w') as questionw, open('mintaka/mintaka_test_answer.txt','w') as answerw:
#     for item in data:
#         # Extract the question and answer strings
#         question_string = item['question']
#         answer_string = item['answer']['mention']
#
#         # print("Question:", question_string)
#         # print("Answer:", answer_string)
#
#         questionw.write(question_string.replace('\n','')+'\n')
#         answerw.write(answer_string.replace('\n','')+'\n')
# print ('Done.')


# extract multihop
with open(mintaka_path) as f:
    data = json.load(f)

with open('mintaka/mintaka_test_question_multihop.txt','w') as questionw, open('mintaka/mintaka_test_answer_multihop.txt','w') as answerw:
    for item in data:
        # Extract the question and answer strings
        if item['complexityType'] == 'multihop':
            question_string = item['question']
            answer_string = item['answer']['mention']

            # print("Question:", question_string)
            # print("Answer:", answer_string)

            questionw.write(question_string.replace('\n','')+'\n')
            answerw.write(answer_string.replace('\n','')+'\n')
print ('Done.')