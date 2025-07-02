from collections import Counter
from dataclasses import dataclass

import string

CHAMPS = [
        'aatrox', 'ahri', 'akali', 'akshan', 'alistar', 'ambessa', 'amumu',
        'anivia', 'annie', 'aphelios', 'ashe', 'aurelionsol', 'aurora',
        'azir', 'bard', 'belveth', 'blitzcrank', 'brand', 'braum', 'briar',
        'caitlyn', 'camille', 'cassiopeia', 'chogath', 'corki', 'darius',
        'diana', 'draven', 'drmundo', 'ekko', 'elise', 'evelynn', 'ezreal',
        'fiddlesticks', 'fiora', 'fizz', 'galio', 'gangplank', 'garen',
        'gnar', 'gragas', 'graves', 'gwen', 'hecarim', 'heimerdinger','hwei',
        'illaoi', 'irelia', 'ivern', 'janna', 'jarvaniv', 'jax', 'jayce',
        'jhin', 'jinx', 'kaisa', 'kalista', 'karma', 'karthus', 'kassadin',
        'katarina', 'kayle', 'kayn', 'kennen', 'khazix', 'kindred', 'kled',
        'kogmaw', 'ksante', 'leblanc', 'leesin', 'leona', 'lillia',
        'lissandra', 'lucian', 'lulu', 'lux', 'malphite', 'malzahar',
        'maokai', 'masteryi', 'mel', 'milio', 'missfortune', 'wukong',
        'mordekaiser', 'morgana', 'naafiri', 'nami', 'nasus', 'nautilus',
        'neeko', 'nidalee', 'nilah', 'nocturne', 'nunuandwillump', 'olaf',
        'orianna', 'ornn', 'pantheon', 'poppy', 'pyke', 'qiyana', 'quinn',
        'rakan', 'rammus', 'reksai', 'rell', 'renataglasc', 'renekton',
        'rengar', 'riven', 'rumble', 'ryze', 'samira', 'sejuani', 'senna',
        'seraphine', 'sett', 'shaco', 'shen', 'shyvana', 'singed', 'sion',
        'sivir', 'skarner', 'smolder', 'sona', 'soraka', 'swain', 'sylas',
        'syndra', 'tahmkench', 'taliyah', 'talon', 'taric', 'teemo', 'thresh',
        'tristana', 'trundle', 'tryndamere', 'twistedfate', 'twitch', 'udyr',
        'urgot', 'varus', 'vayne', 'veigar', 'velkoz', 'vex', 'vi', 'viego',
        'viktor', 'vladimir', 'volibear', 'warwick', 'xayah', 'xerath',
        'xinzhao', 'yasuo', 'yone', 'yorick', 'yuumi', 'zac', 'zed', 'zeri',
        'ziggs', 'zilean', 'zoe', 'zyra',
    ]


@dataclass
class Champion:
    name: str
    unique_chars: set[str]


class BestTeamsFinder:
    """
    Single-use class used to find teams with the best alphabet coverage.
    Teams are built up to the specified size using the provided names.

    Call the `solve` method to generate results.
    """

    def __init__(self, champ_names: list[str], team_size: int):
        self._team_size = team_size

        normalized_names = self._normalize_names(champ_names)
        char_freq = self._compute_char_frequencies(normalized_names)
        char_rarity_scores = self._compute_char_rarity_scores(char_freq)

        self._champs = self._create_champion_objects(normalized_names)
        self._champs.sort(
            key=lambda champ: sum(char_rarity_scores[c] for c in champ.unique_chars),
            reverse=True,
        )

        self._unique_chars_for_suffix = self._compute_unique_chars_for_suffixes(
            self._champs
        )

        self._best_unique_char_count = 0
        self._best_teams = []

    def solve(self) -> list[list[Champion]]:
        """
        Finds the best teams maximizing unique character coverage.

        Returns:
            List of best teams found. Each team is a list of champions.
        """
        # Start search with all champs available + empty initial team
        self._recurse(0, [], set())

        return self._best_teams

    def _recurse(
        self, idx: int, current_team: list[Champion], current_unique_chars: set[str]
    ) -> None:
        """
        Recursively search for teams, using specified state as the start.

        Args:
            idx: Marks the remaining champs we can use from _champs during the search
            current_team: Currently selected champions.
            current_unique_chars: Set of unique letters for current_team.
        """
        # Compare completed team against existing candidates
        if len(current_team) == self._team_size:
            unique_char_count = len(current_unique_chars)
            if unique_char_count > self._best_unique_char_count:
                self._best_unique_char_count = unique_char_count
                self._best_teams = [current_team[:]]
            elif unique_char_count == self._best_unique_char_count:
                self._best_teams.append(current_team[:])
            return

        # Prune if there aren't enough remaining champs to complete the team
        if (
            idx >= len(self._champs)
            or len(current_team) + (len(self._champs) - idx) < self._team_size
        ):
            return

        # Prune if current team's letters + all remaining letters available can't beat/equal best found so far
        max_possible_chars = current_unique_chars | self._unique_chars_for_suffix[idx]
        if len(max_possible_chars) < self._best_unique_char_count:
            return

        # Try adding each remaining champ to current team and continue search
        for next_idx in range(idx, len(self._champs)):
            new_champ = self._champs[next_idx]
            new_unique_chars = current_unique_chars | new_champ.unique_chars
            self._recurse(next_idx + 1, current_team + [new_champ], new_unique_chars)

    def _normalize_names(self, champs: list[str]) -> list[str]:
        """Given a list of names, lowercase them and filter for alphabet letters only"""
        return ["".join(filter(str.isalpha, name.lower())) for name in champs]

    def _compute_char_frequencies(self, names: list[str]) -> Counter:
        """Count letters by how many names it appears in."""
        return Counter(char for name in names for char in set(name))

    def _compute_char_rarity_scores(self, freqs: Counter[str]) -> dict[str, float]:
        """Generate rarity scores based on character frequncies."""
        # The **100 beneficially exaggerates the value of rarer characters.
        return {char: 1 / (freq**100) for char, freq in freqs.items()}

    def _create_champion_objects(self, names: list[str]) -> list[Champion]:
        return [
            Champion(
                name=name,
                unique_chars=set(name),
            )
            for name in names
        ]

    def _compute_unique_chars_for_suffixes(
        self, champs: list[Champion]
    ) -> list[set[str]]:
        """Returns a list such that at index `i`, we have the set of unique characters for the suffix `champs[i:]`"""
        suffix_sets = []
        acc = set()
        for champ in reversed(champs):
            acc |= champ.unique_chars
            suffix_sets.append(acc.copy())
        suffix_sets.reverse()
        return suffix_sets


if __name__ == "__main__":
    team_size = 5  # adjust as desired
    champ_names = CHAMPS  # could use e.g. list of full champ titles instead of CHAMPS
    solver = BestTeamsFinder(champ_names, team_size)
    best_teams = solver.solve()

    # Display best teams and their missing letters
    for i, team in enumerate(best_teams):
        print(f"Team {i + 1}:")
        print("\n".join(champ.name for champ in team))
        used_chars = set.union(*(champ.unique_chars for champ in team))
        missing_chars = "".join(sorted(set(string.ascii_lowercase) - used_chars))
        print(f"missing chars: {len(missing_chars)} ({missing_chars})")
        print()
