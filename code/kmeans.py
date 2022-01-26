"""
This is a simple application for sentence embeddings: clustering
Sentences are mapped to sentence embeddings and then k-mean clustering is applied.
"""
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def read_nli_dataset(file):
  texts = []
  labels = []
  with io.open(file, encoding = 'utf-8') as f:
    for line in f:
      toks = line.strip().split(' ## ')
      texts.append(toks[0].split('\t'))
      labels.append(toks[1])
  
  return texts, labels

train_texts, train_labels = read_nli_dataset('data/TOEFL_bert_train.txt')
test_texts, test_labels = read_nli_dataset('data/TOEFL_bert_test.txt')

all_texts = []

for text in train_texts:
  for sent in text:
    all_texts.append(sent)

for text in test_texts:
  for sent in text:
    all_texts.append(sent)

# Corpus with example sentences
corpus = ['A man is eating food.',
          'A man is eating a piece of bread.',
          'A man is eating pasta.',
          'The girl is carrying a baby.',
          'The baby is carried by the woman',
          'A man is riding a horse.',
          'A man is riding a white horse on an enclosed ground.',
          'A monkey is playing drums.',
          'Someone in a gorilla costume is playing a set of drums.',
          'A cheetah is running behind its prey.',
          'A cheetah chases prey on across a field.'
          ]
corpus_embeddings = embedder.encode(all_texts)

# Perform kmean clustering
num_clusters = 11
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_

clustered_sentences = [[] for i in range(num_clusters)]
for sentence_id, cluster_id in enumerate(cluster_assignment):
    clustered_sentences[cluster_id].append(corpus[sentence_id])

for i, cluster in enumerate(clustered_sentences):
    print("Cluster ", i+1)
    print(cluster)
    print("")