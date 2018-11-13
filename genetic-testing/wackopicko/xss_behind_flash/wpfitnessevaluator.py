import re
import pylev
import stringguess


class FitnessEvaluator:
    MAX = 10

    base = MAX
    correction = 0

    domain = [".*(<script>alert\('.*'\)<\/script>).*|.*(<script>alert\(\d+\)<\/script>).*"]


    def evaluate(self, selenium_mock, inner_individuals):

        self.base = selenium_mock.base

        self.correction = 0

        page = selenium_mock.current_page
        
        if self.base == 1:
            payload = selenium_mock.payload
            inner_individuals, best = stringguess.main(
                target=payload,
                domain=self.domain,
                population=inner_individuals
            )
            f = best.fitness.values[0]
            print("{} <{}> {}".format(payload, f, "".join(best)))
            # print("Matching:  {}".format("".join(best)))

            self.correction = 1 / (1 + f)
            # self.correction = 1 / (1 + pylev.levenshtein(payload, self.TARGET))
            # print(payload)

        return inner_individuals, self.base - self.correction
