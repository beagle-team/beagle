import re
import pylev
import stringguess


class FitnessEvaluator:
    MAX = 10

    base = MAX
    correction = 0

    domain = [".*(<script>alert\('.*'\)</script>).*|.*(<script>alert\(\d+\)</script>).*"]

    def evaluate(self, selenium_mock, inner_individuals):

        page = selenium_mock.current_page

        payload = selenium_mock.username_session

        # Evaluate CFG
        if page == 'signup.php':
            self.base = 3
        elif page == 'confirm.php':
            self.base = 2
        elif page == 'welcome.php':
            self.base = 1

        # Evaluate Contracts
        if page == 'signup.php':
            if len(payload) > 6 and re.search(r"\d", payload) is not None:
                self.correction = 0.5

        if page == 'confirm.php':
            self.correction = 0

        if page == 'welcome.php':
            inner_individuals, best = stringguess.main(
                target=payload,
                domain=self.domain,
                population=inner_individuals
            )
            f = best.fitness.values[0]
            print("{} >{}<  {}".format(payload, f, "".join(best)))

            self.correction = 1 / (1 + f)
            # self.correction = 1 / (1 + pylev.levenshtein(payload, self.TARGET))
            # print(payload)

        return inner_individuals, self.base - self.correction
