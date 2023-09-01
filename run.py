
def fetch_hacker_news_stories():
    keywords = ["job", "employment", "employ", "opportunity", "tech stack", "technology", "technologies", "salary", "future", "trend", "python", ".py", "js", "techstackjobs"]

    print("fetch_hacker_news_stories")
    url = "https://hacker-news.firebaseio.com/v0/newstories.json"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            response_json = response.json()
            messages = []
            for item in response_json:
                try:
                    item_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item}.json")
                    if item_response.status_code == 200:
                        obj = item_response.json()
                        # Calculate the time difference (in hours) from the current time
                        current_time = time.time()
                        time_difference_hours = (current_time - obj["time"]) / 3600
                        initial_score = 0

                        # Count the number of keywords in the title
                        title_lower = obj["title"].lower()
                        keyword_count = sum(keyword in title_lower for keyword in keywords)
                        initial_score += keyword_count

                        if "url" in obj:
                            keyword_count += sum(keyword in obj["url"] for keyword in keywords)
                        if "text" in obj:
                            keyword_count += sum(keyword in obj["text"].lower() for keyword in keywords)

                        initial_score = keyword_count
                        # Adjust the score based on the time condition
                        if time_difference_hours < 1 and obj["score"] >= 10:
                            initial_score *= 3

                        if initial_score > 0:
                            obj["kids"] = None
                            messages.append({
                                "keyword_count": keyword_count,
                                "initial_score": initial_score,
                                "obj": obj,
                                "forum_link": f"https://news.ycombinator.com/item?id={item}"
                            })

                except:
                    print("Exception")
            
            sorted_messages = sorted(messages, key=lambda x: (-x["initial_score"], x["keyword_count"]))
            json_string = json.dumps(sorted_messages, indent=4)

            sent = send_mail(
                'Hacker News Keyword Report',
                json_string,
                "example@gmail.com",
                ["example@gmail.com"],
                fail_silently=False,
            )
        else:
            print("fetch_hacker_news_stories failed with code: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        # Handle network or request-related errors
        print("Request Exception")
