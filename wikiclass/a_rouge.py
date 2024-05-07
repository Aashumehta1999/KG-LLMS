from rouge import Rouge

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def get_rouge(pred,truth):
    rouge = Rouge()

    # Assuming each file has the same number of lines
    scores = []
    for ref, hyp in zip(pred, truth):
        score = rouge.get_scores(hyp, ref)
        scores.append(score)

    # Calculate average scores
    average_scores = dict()
    for score in scores:
        for key in score[0]:
            if key not in average_scores:
                average_scores[key] = []
            average_scores[key].append(score[0][key]['f'])

    for key in average_scores:
        average_scores[key] = sum(average_scores[key]) / len(average_scores[key])

    print("Average ROUGE scores:", average_scores)


def get_match(ref,hyp):
    # if mentioned
    ref= ref.lower().strip()
    hyp=hyp.lower().strip()
    # import pdb;pdb.set_trace()
    if ref in hyp:
        return 1.
    else:
        return 0.

def get_accuracy(pred,truth):
    scores = []
    for ref, hyp in zip(pred, truth):
        score = get_match(hyp, ref)
        scores.append(score)
    acc = sum(scores)/len(scores)

    print("Accuracy :", acc)

if __name__ == "__main__":
    # pred = read_file('mintaka_res/t2.llama.txt')[:1000]
    # truth = read_file('mintaka/mintaka_test_answer.txt')[:1000]
    pred = read_file('mintaka_res/t2.llama_multihop.txt')
    truth = read_file('mintaka/mintaka_test_answer_multihop.txt')
    get_accuracy(pred,truth)
    get_rouge(pred,truth)

'''


rouge = Rouge()
ref='Adam Sandler'
hyp='  Adam Sandler has more kids.'
hyp1='  Adam Sandler '
score = rouge.get_scores(hyp1, ref)
print(get_accuracy(ref,hyp1))




Test 1k
Accuracy : 0.515
Average ROUGE scores: {'rouge-1': 0.28567794201435776, 'rouge-2': 0.1432060432084881, 'rouge-l': 0.28436602509884873}


Multihop 400
Accuracy : 0.445
Average ROUGE scores: {'rouge-1': 0.2439109606666336, 'rouge-2': 0.13636874007924202, 'rouge-l': 0.24283827896237292}

'''

