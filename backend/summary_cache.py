class SummaryCache():
    def __init__(self):
        self.cache = {}

    def add_to_cache(self, key: str, summary: str):
        self.cache[key] = summary

    def remove_from_cache(self, key: str):
        if self.in_cache(key):
            self.cache.pop(key)

    def get_from_cache(self, key: str) -> str:
        return self.cache.get(key, None)

    def in_cache(self, key: str) -> bool:
        return key in self.cache