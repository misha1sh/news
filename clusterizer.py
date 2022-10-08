from tqdm.notebook import tqdm
import math
import collections
import hdbscan
import numpy as np

def dist(d1, d2):
    s = 0
    for w in d1["short"] & d2["short"]:
        # s += 1.
        # s += math.log2(d1["long"][w]["count"] * d2["long"][w]["count"] + 10)
        s += d1["long"][w]["count"] * d2["long"][w]["count"]
    return max(500 - s, 0)
        # return math.log2(max(300 - s, 0) + 1)

def calc_distances(popular_keywords):
    distances = []
    # for i in tqdm(range(len(popular_keywords))):
    for i in range(len(popular_keywords)):
        document = popular_keywords[i]
        d = []
        for j in range(len(popular_keywords)):
            if i == j:
                d.append(0)
            elif i > j:
                d.append(distances[j][i])
            else:
                document2 = popular_keywords[j]
                d.append(dist(document, document2))
        distances.append(d)
    return distances

# from sklearn.cluster import DBSCAN
# import numpy as np
# distances = np.array(distances)
# clustering = DBSCAN(eps=3, min_samples=2, metric='precomputed').fit(distances)
# labels = clustering.labels_

def clustering_score(labels):
    score = 0
    counter = collections.Counter(labels)
    for label, count in counter.most_common(100):
        if label == -1: continue
        if count > 10 and count < 30:
            score += 2
        score += 1
    return score
    

def clusterize_labels(popular_keywords, distances):
    clusterer = hdbscan.HDBSCAN(metric='precomputed')
    distances = np.array(distances)
    clustering = clusterer.fit(distances)

    clustering_scores = []
    for i in range(0, 500):
        labels = clustering.single_linkage_tree_.get_clusters(i, min_cluster_size=3)
        score = clustering_score(labels)
        clustering_scores.append(score)

    i = np.argmax(clustering_scores)
    # print("optimal_clustering", i)
    labels = clustering.single_linkage_tree_.get_clusters(i, min_cluster_size=3)

    return labels


   
def dist_most_common(d):
    s = 0
    from collections import defaultdict
    words = defaultdict(lambda:0)
    for i in range(len(d)):
        for j in range(i + 1, len(d)):
            d1 = d[i]
            d2 = d[j]
            for w in d1["short"] & d2["short"]:
                words[w] += d1["long"][w]["count"] * d2["long"][w]["count"]
                
    words = list(words.items())
    words.sort(key=lambda w: -w[1])
    return words[:10]


def clusterize(data, popular_keywords, count=3, debug=False):
    distances = calc_distances(popular_keywords)
    labels = clusterize_labels(popular_keywords, distances)
    counter = collections.Counter(labels)
    
    res = []
    
    for label, count in counter.most_common(8):
        if label == -1:
            continue
        if debug: print("cluster: ", label, " count=", count)
        # ddocs = []
        ddocs_i = []
        dpopular_keywords = []
        for i in range(len(popular_keywords)):
            if labels[i] == label:
                # ddocs.append(keyword_groups[i])
                ddocs_i.append(i)
                dpopular_keywords.append(popular_keywords[i])

        distances_i = []
        for i in ddocs_i:
            d = 0
            for j in ddocs_i:
                d += distances[i][j]
            distances_i.append((d, i))
        distances_i.sort(key=lambda i: i[0])  
        
        for score, i in distances_i[:3]:
            art = data[i]
            if debug: print(art["title"], art["url"])
            
        if len(res) < count and len(distances_i) > 0:
            score, i = distances_i[0]
            res.append(data[i])

        if debug: display(dict(dist_most_common(dpopular_keywords)))
        # display(most_popular_keywords(keywords_mean(ddocs), 10))

        if debug: print("\n")
        
        
    return res