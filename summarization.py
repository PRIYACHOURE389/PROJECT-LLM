import openai

def summarize_article(article_text):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"Summarize the following news article:\n\n{article_text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary could not be generated."
