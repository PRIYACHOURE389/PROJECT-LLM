import openai

def summarize_article(article_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model for chat completions
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following news article:\n\n{article_text}"}
            ],
            max_tokens=150,
            temperature=0.7  # Adjust as needed
        )
        summary = response.choices[0].message['content'].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary could not be generated."

# Example usage
article_text = "Your article text here."
summary = summarize_article(article_text)
print(summary)
