# Help on how to graph/quantify political opinions from: https://www.storybench.org/ten-ways-you-might-consider-visualizing-political-issues-and-ideologies-this-election/

# TO DO: Write basic class outline that stores a person's name, politic allignment, and position on political compass or however I best think is right data
# Current Note: seems like political compass is the best way to measure it right now. Might just implement in as a label in user object
class Politic:
    def __init__(self, user, political_score, political_affiliation):
        self.user = user  # The user associated with this politics data, primary key
        self.political_score = political_score
        self.political_affiliation = political_affiliation