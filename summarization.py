import openai
from newsapi import NewsApiClient

# Set OpenAI API key
openai.api_key = "sk-CeO8TeSgyrNL6JhdFL1RMLvisTjDIOuOoAANg05tbHT3BlbkFJBNuiZkRhqoIndOuzdphPWyeexXjsVT8-evKzceawsA"

# Set NewsAPI key
newsapi = NewsApiClient(api_key="01502dbf80e8480681d88df694c2e155")

# Example function to summarize an article
def summarize_article(article_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following news article:\n\n{article_text}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary could not be generated."

# Example of how to use the NewsAPI client
articles = newsapi.get_top_headlines(q="technology")
for article in articles['articles']:
    summary = summarize_article(article['content'])
    print(f"Original: {article['content']}\nSummary: {summary}\n")
