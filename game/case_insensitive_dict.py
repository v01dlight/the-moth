class CaseInsensitiveDict(dict):
    def __init__(self, seed):
        self.case_sensitive = seed
        super().__init__({
            key.upper(): seed[key]
            for key in seed
        })

    def __getitem__(self, k):
        return super().__getitem__(k.upper())

    def __setitem__(self, k, v):
        self.case_sensitive[k] = v
        super().__setitem__(k.upper(), v)

    def __contains__(self, k):
        return super().__contains__(k.upper())

    def keys(self):
        return self.case_sensitive.keys()
