import os
import random
import re
import sys
import math
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages
def pages_gen(corpus):
    pages = dict()
    for key,vals in corpus.items():
        if key not in pages.keys():
            pages[key] = 0 #adding unique page to pages dict
        for val in vals:
            if val not in pages.keys():
                pages[val] = 0
    return pages
def sample_gen_iterative(corpus,n):
    pages = dict()
    for key,vals in corpus.items():
        if key not in pages.keys():
            pages[key] = 1/n
        for val in vals:
            if val not in pages.keys():
                pages[val] = 1/n
    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    rem_probability = 1-damping_factor
    pages = pages_gen(corpus)

    equal_probablity_each = rem_probability/(len(pages.keys()))
    for key in pages.keys():
        pages[key] += equal_probablity_each
        if key == page:
            links_page = corpus[key]
            # print(links_page)
            probability_by_damping = damping_factor/len(links_page)
            # print(probability_by_damping)
            for link in links_page:
                #adding probability
                pages[link] += probability_by_damping

    return pages



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = pages_gen(corpus)
    for i in range(n):
        if i == 0:
            options = list(corpus.keys())
            sample = random.choices(options).pop()
            # print(type(samples))
            samples[sample] =samples[sample] +1
        else:
            next_prob = transition_model(corpus,sample,damping_factor)
            next_prob_options = list(next_prob.keys())
            weights = [next_prob[key] for key in next_prob_options]
            # print("weights: ",weights)
            sample = random.choices(next_prob_options,weights).pop()
            # print(sample)
            samples[sample] += 1
    #calculating probability
    for key in  samples.keys():
        samples[key] /= n

    return samples

def count_page(corpus):
    result =set()
    for key,vals in corpus.items():
        result.add(key)
        for val in vals:
            result.add(val)
    # print(result)

    return len(result)




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n=count_page(corpus)
    samples=sample_gen_iterative(corpus,n)
    error = 1 #initial error
    while error>=0.001:
        #reset error
        error = 0
        #copy samples
        pre_sample= samples.copy()
        for sample in samples.keys():
            # print(sample)
            parents =[]
            for link in corpus.keys():
                if sample in corpus[link]:
                    parents.append(link)
            #damping_factor
            prob_d = 0
            if len(parents) != 0:
                for parent in parents:
                    numlinks = len(corpus[parent])
                    prob_d += pre_sample[parent]/numlinks
            samples[sample] = (1-damping_factor)/n + damping_factor*prob_d
            #calculate change
            new_error = abs(samples[sample]-pre_sample[sample])
            if error <new_error:
                error = new_error
    return samples








if __name__ == "__main__":
    main()
