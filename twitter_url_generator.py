class TwitterUrlGenerator:
    def __init__(self, city):
        self.city = city

    def generate_url(self, query_string=None):
        if query_string is None:
            return f"https://twitter.com/search?q=verified+{self.city}+%28bed+OR+beds+OR+icu+OR+oxygen+OR+ventilator+OR+ventilators+OR+test+OR+tests+OR+testing+OR+fabiflu+OR+remdesivir+OR+favipiravir+OR+tocilizumab+OR+plasma+OR+tiffin+OR+food%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live"
        else:
            return f"https://twitter.com/search?q=verified+{self.city}+%28{query_string}%29+-%22not+verified%22+-%22unverified%22+-%22needed%22+-%22need%22+-%22needs%22+-%22required%22+-%22require%22+-%22requires%22+-%22requirement%22+-%22requirements%22&f=live"

    @classmethod
    def format_url_as_html(cls, url):
        return f"<a href='{url}'>Click Here</a> to view the results."


if __name__ == "__main__":
    url = TwitterUrlGenerator(city="delhi").generate_url()
    print(TwitterUrlGenerator.format_url_as_html(url))
