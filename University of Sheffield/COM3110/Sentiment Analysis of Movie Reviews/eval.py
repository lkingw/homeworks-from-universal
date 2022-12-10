import subprocess

base_cmd = [ "python", "NB_sentiment_analyser.py" ]

res = subprocess.run(base_cmd + [ "./datasets/train.tsv", "./datasets/dev.tsv", "./datasets/test.tsv", "-classes", "5", "-output_files"], stdout=subprocess.PIPE)
resstr = res.stdout.decode("utf-8").strip()
print(resstr)

res = subprocess.run(base_cmd + [ "./datasets/train.tsv", "./datasets/dev.tsv", "./datasets/test.tsv", "-classes", "3", "-output_files", "-confusion_matrix"], stdout=subprocess.PIPE)
resstr = res.stdout.decode("utf-8").strip()
print(resstr)