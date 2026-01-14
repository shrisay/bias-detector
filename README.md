# bias-detector

Created this as a way to detect biased languaged in news articles, since I noticed it an issue during my MUN research. 

Further details:  
- Used Python’s Django framework and newspaper3k to scrape articles for text
- Classifies bias into 4 custom categories: nationalistic, sensational, religious/cultural, or neutral
- Trained a roBERTa-based model on a custom dataset of 700+ sentences
- Currently developing into a browser extension for easy use
