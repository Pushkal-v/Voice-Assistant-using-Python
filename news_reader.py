import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NewsReader:
    def __init__(self):
        self.api_key = os.getenv('GNEWS_API_KEY')
    
    def get_news(self, topic="general", max_articles=3):
        """Get news headlines - NOW WORKING!"""
        try:
            url = f"https://gnews.io/api/v4/top-headlines?category={topic}&lang=en&max={max_articles}&apikey={self.api_key}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if not articles:
                    return ["No news articles found right now"]
                
                headlines = []
                for i, article in enumerate(articles[:max_articles], 1):
                    title = article.get('title', 'No title').split(' - ')[0]
                    headlines.append(f"{i}. {title}")
                
                return headlines
            else:
                return [f"News service temporarily unavailable"]
                
        except Exception as e:
            return [f"Could not fetch news: {str(e)}"]
    
    def format_news_response(self, news_items, topic="general"):
        """Format news for speaking"""
        if not news_items or "Error" in news_items[0]:
            return "Sorry, I couldn't fetch the news at the moment"
        
        response = f"Here are the latest {topic} news headlines. "
        response += ". ".join(news_items)
        return response
    
    def extract_topic(self, command):
        """Extract news topic from command - WORKING!"""
        topic_mapping = {
            'technology': 'technology', 'tech': 'technology', 'computer': 'technology',
            'sports': 'sports', 'sport': 'sports', 'game': 'sports', 'football': 'sports',
            'business': 'business', 'finance': 'business', 'economy': 'business',
            'science': 'science', 'research': 'science',
            'health': 'health', 'medical': 'health', 'medicine': 'health',
            'entertainment': 'entertainment', 'movie': 'entertainment', 'music': 'entertainment',
            'general': 'general', 'news': 'general', 'headlines': 'general'
        }
        
        command = command.lower()
        for keyword, topic in topic_mapping.items():
            if keyword in command:
                return topic
        
        return 'general'
   

def main():
    """Test the news reader functionality"""
    print("=== Testing News Reader ===")
    
  
    news_reader = NewsReader()
    
    
    if not news_reader.api_key:
        print("❌ Error: GNEWS_API_KEY not found in .env file")
        print("Please make sure your .env file contains:")
        print("GNEWS_API_KEY=your_actual_api_key_here")
        return
    
    print("✅ API key loaded successfully")
    
    
    test_topics = ['general', 'technology', 'sports', 'business', 'health']
    
    for topic in test_topics:
        print(f"\n📰 Testing {topic} news:")
        news_items = news_reader.get_news(topic=topic)
        
        if news_items:
            for item in news_items:
                print(f"   {item}")
            
          
            formatted = news_reader.format_news_response(news_items, topic)
            print(f"\n   Formatted for speech: {formatted[:100]}...")
        else:
            print("   No news items returned")
    
   
    print("\n🎯 Testing topic extraction:")
    test_commands = [
        "tech news",
        "sports headlines",
        "business updates",
        "health news",
        "tell me the latest news"
    ]
    
    for command in test_commands:
        topic = news_reader.extract_topic(command)
        print(f"   '{command}' → '{topic}'")

if __name__ == "__main__":
    main()