import pymupdf
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
 
# Load pre-trained model tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def summarizer(text, keywords, lines):
    def preprocess_text(text):
        sentences = text.split('. ')
        return sentences
    
    def get_sentence_embeddings(sentences, tokenizer, model):
        embeddings = []
        for sentence in sentences:
            inputs = tokenizer(sentence, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
        return embeddings
    
    def rank_sentences(sentences, embeddings):
        sentence_scores = []
        for i, emb in enumerate(embeddings):
            score = cosine_similarity([emb], embeddings).mean()
            sentence_scores.append((score, i))
        ranked_sentences = sorted(sentence_scores, reverse=True, key=lambda x: x[0])
        return [sentences[i] for _, i in ranked_sentences]
    
    def keyword_relevant_sentences(sentences, keywords):
        relevant_sentences = []
        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                relevant_sentences.append(sentence)
        return relevant_sentences
    
    def summarize(text, keywords, num_sentences=30):
        sentences = preprocess_text(text)
        embeddings = get_sentence_embeddings(sentences, tokenizer, model)
        ranked_sentences = rank_sentences(sentences, embeddings)
        
        summary = ranked_sentences[:num_sentences]
        relevant_sentences = keyword_relevant_sentences(sentences, keywords)
        
        # Ensure unique sentences in the final summary
        final_summary_sentences = list(dict.fromkeys(summary + relevant_sentences))
        
        # Maintain the original order
        final_summary_sentences_sorted = sorted(final_summary_sentences, key=lambda x: sentences.index(x))
        
        return '. '.join(final_summary_sentences_sorted)
    
    # Example usage
    # text = """Your input text goes here. It should be a long paragraph with multiple sentences."""
    # keywords = ["keyword1", "keyword2"]
    
    # summary = summarize(text, keywords)
    # print("Summary:", summary)
    
    # text = """Climate change is one of the most pressing issues of our time. Rising global temperatures have led to a variety of environmental impacts, including more frequent and severe weather events. The polar ice caps are melting at an alarming rate, causing sea levels to rise and threatening coastal communities. Additionally, changing weather patterns are affecting agriculture, making it more difficult for farmers to grow crops. Governments and organizations around the world are working to address climate change through various measures. Renewable energy sources, such as solar and wind power, are being developed to reduce reliance on fossil fuels. International agreements, like the Paris Agreement, aim to unite countries in the fight against climate change. Public awareness and education on the issue are also crucial for driving change. It is essential that everyone takes part in efforts to mitigate the effects of climate change to ensure a sustainable future for generations to come."""
    # import pymupdf
    
    # extracted_text = ""
    # file_name = file.name
    # doc = pymupdf.open(f"{file}") # open a document
    # for page in doc: # iterate the document pages
    #     extracted_text += page.get_text() # get plain text encoded as UTF-8
    
    # keywords = ["threat", "ransomware"]
    
    summary = summarize(text, keywords, lines)
    # print("Summary:", summary)
    print(keywords, lines)

    return summary


if __name__ == "__main__":
    
    extracted_text = ""
    # doc = pymupdf.open("first_chapter.pdf") # open a document
    for page in doc: # iterate the document pages
        extracted_text += page.get_text() # get plain text encoded as UTF-8
    
    keywords = ["threat", "ransomware"]
    lines = 30
    print(summarizer(extracted_text,keywords,lines))
    
