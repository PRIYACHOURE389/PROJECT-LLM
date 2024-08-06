import json
import os

# Directory for the config folder
config_dir = 'config'
# Path for the sample_articles.json file
sample_articles_path = os.path.join(config_dir, 'sample_articles.json')

# Sample articles data
articles = [
    {"title": "Equity Markets Rally", "description": "Equity markets showed a significant rally today...", "content": "Equity markets rallied today due to positive economic data..."},
    {"title": "Tech Stocks Soar", "description": "Tech stocks saw a major increase in value...", "content": "Tech stocks soared today after several companies reported strong earnings..."},
    {"title": "Healthcare Sector Growth", "description": "The healthcare sector experienced growth...", "content": "The healthcare sector grew significantly as new advancements were made..."},
    {"title": "Energy Prices Rise", "description": "Energy prices have seen an upward trend...", "content": "Energy prices increased due to higher demand and supply constraints..."},
    {"title": "Consumer Spending Increases", "description": "Consumer spending has shown an increase...", "content": "Consumer spending rose as confidence in the economy improved..."},
    {"title": "Automotive Industry Trends", "description": "New trends are emerging in the automotive industry...", "content": "The automotive industry is seeing trends such as electric vehicle adoption..."},
    {"title": "Real Estate Market Fluctuations", "description": "The real estate market has been fluctuating...", "content": "Fluctuations in the real estate market are attributed to interest rate changes..."},
    {"title": "Retail Sector Performance", "description": "The retail sector's performance is under scrutiny...", "content": "Retail sector performance varies with changes in consumer behavior..."},
    {"title": "Financial Services Innovation", "description": "Innovation in financial services is driving growth...", "content": "Financial services are innovating with new technologies and services..."},
    {"title": "Telecommunications Advances", "description": "Telecommunications is advancing rapidly...", "content": "Advancements in telecommunications include 5G deployment and IoT integration..."},
    {"title": "Travel and Tourism Recovery", "description": "The travel and tourism sector is recovering...", "content": "Recovery in travel and tourism is evident as restrictions ease and demand increases..."},
    {"title": "Agriculture Sector Developments", "description": "New developments in agriculture are promising...", "content": "Developments in agriculture include sustainable farming practices..."},
    {"title": "Pharmaceutical Innovations", "description": "Innovations in pharmaceuticals are noteworthy...", "content": "Pharmaceutical innovations are leading to new treatments and medications..."},
    {"title": "Media Industry Evolution", "description": "The media industry is evolving rapidly...", "content": "Evolution in the media industry includes shifts to digital platforms..."},
    {"title": "Aerospace Industry Growth", "description": "Growth in the aerospace industry is notable...", "content": "The aerospace industry is growing due to increased travel and defense spending..."},
    {"title": "Education Sector Changes", "description": "Changes in the education sector are significant...", "content": "Significant changes in education include the rise of online learning..."},
    {"title": "Hospitality Industry Trends", "description": "Trends in the hospitality industry are emerging...", "content": "Emerging trends in hospitality include personalized guest experiences..."},
    {"title": "Food and Beverage Industry Shifts", "description": "The food and beverage industry is shifting...", "content": "Shifts in the food and beverage industry include increased demand for healthy options..."},
    {"title": "Transportation Sector Dynamics", "description": "Dynamics in the transportation sector are changing...", "content": "Changes in transportation dynamics include the rise of electric vehicles..."},
    {"title": "Manufacturing Industry Outlook", "description": "The outlook for the manufacturing industry is positive...", "content": "A positive outlook for manufacturing is driven by technological advancements..."},
    {"title": "Insurance Sector Innovations", "description": "Innovations in the insurance sector are impactful...", "content": "Impactful innovations in insurance include new risk assessment tools..."},
    {"title": "Mining Industry Developments", "description": "Developments in the mining industry are ongoing...", "content": "Ongoing developments in mining include new extraction technologies..."},
    {"title": "Construction Industry Challenges", "description": "The construction industry faces challenges...", "content": "Challenges in construction include material shortages and regulatory changes..."},
    {"title": "Textile Industry Trends", "description": "Trends in the textile industry are evolving...", "content": "Evolving trends in textiles include sustainable and eco-friendly materials..."},
    {"title": "Logistics and Supply Chain Management", "description": "Management of logistics and supply chains is crucial...", "content": "Effective supply chain management is critical to meet demand and avoid disruptions..."},
    {"title": "Chemical Industry Innovations", "description": "Innovations in the chemical industry are noteworthy...", "content": "Noteworthy innovations in chemicals include new production processes..."},
    {"title": "Metals and Mining Sector Growth", "description": "Growth in metals and mining is observable...", "content": "Observable growth in metals and mining is driven by increased demand..."},
    {"title": "Utilities Sector Performance", "description": "Performance in the utilities sector varies...", "content": "Variations in utilities performance are influenced by regulatory changes..."},
    {"title": "Food Processing Industry", "description": "The food processing industry is evolving...", "content": "Evolutions in food processing include new preservation techniques..."},
    {"title": "Biotechnology Advancements", "description": "Advancements in biotechnology are significant...", "content": "Significant advancements in biotechnology are leading to new medical treatments..."},
    {"title": "Petrochemical Industry Trends", "description": "Trends in the petrochemical industry are emerging...", "content": "Emerging trends in petrochemicals include increased recycling efforts..."},
    {"title": "Defense Industry Developments", "description": "Developments in the defense industry are noteworthy...", "content": "Noteworthy developments in defense include new technologies and strategies..."},
    {"title": "Public Sector Changes", "description": "Changes in the public sector are significant...", "content": "Significant changes in the public sector include new policy implementations..."},
    {"title": "Private Equity Trends", "description": "Trends in private equity are shifting...", "content": "Shifting trends in private equity include increased focus on sustainable investments..."},
    {"title": "Venture Capital Insights", "description": "Insights into venture capital are valuable...", "content": "Valuable insights into venture capital include trends in funding and investment..."},
    {"title": "Startup Ecosystem Growth", "description": "Growth in the startup ecosystem is rapid...", "content": "Rapid growth in startups is driven by innovation and investment..."},
    {"title": "Corporate Governance Practices", "description": "Corporate governance practices are evolving...", "content": "Evolving corporate governance practices include increased transparency..."},
    {"title": "Investment Banking Trends", "description": "Trends in investment banking are emerging...", "content": "Emerging trends in investment banking include new financial products..."},
    {"title": "Economic Policy Changes", "description": "Changes in economic policy are significant...", "content": "Significant changes in economic policy include new tax regulations..."},
    {"title": "Social Media Industry Dynamics", "description": "Dynamics in the social media industry are changing...", "content": "Changing dynamics in social media include increased focus on user privacy..."},
    {"title": "Luxury Goods Market", "description": "The luxury goods market is evolving...", "content": "Evolutions in luxury goods include new trends and consumer preferences..."},
    {"title": "E-commerce Sector Performance", "description": "Performance in the e-commerce sector is notable...", "content": "Notable performance in e-commerce is driven by increased online shopping..."},
    {"title": "Renewable Energy Developments", "description": "Developments in renewable energy are promising...", "content": "Promising developments in renewable energy include new technologies and projects..."},
    {"title": "Automobile Manufacturing Innovations", "description": "Innovations in automobile manufacturing are noteworthy...", "content": "Noteworthy innovations in automobiles include new production methods..."},
    {"title": "Consumer Electronics Trends", "description": "Trends in consumer electronics are evolving...", "content": "Evolving trends in electronics include new gadgets and smart devices..."},
    {"title": "Textile Manufacturing Advances", "description": "Advances in textile manufacturing are significant...", "content": "Significant advances in textiles include new materials and production techniques..."},
    {"title": "Semiconductor Industry Outlook", "description": "The outlook for the semiconductor industry is positive...", "content": "A positive outlook for semiconductors is driven by high demand for chips..."},
    {"title": "Automotive Supply Chain", "description": "Supply chain issues in the automotive industry are being addressed...", "content": "Efforts to address supply chain issues in automotive include new strategies..."},
    {"title": "Telecom Industry Regulations", "description": "Regulations in the telecom industry are changing...", "content": "Changing regulations in telecom include new compliance requirements..."}
]


# Write the sample articles to a JSON file
try:
    os.makedirs(config_dir, exist_ok=True)
    with open(sample_articles_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4)
    print(f"Sample articles written to {sample_articles_path}")
except Exception as e:
    print(f"Error creating sample_articles.json: {e}")
