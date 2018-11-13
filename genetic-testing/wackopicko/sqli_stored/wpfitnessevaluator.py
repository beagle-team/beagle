import re
import pylev
import stringguess
import regguess


class FitnessEvaluator:
    MAX = 10
    base = MAX
    correction = 0

    reg_domain = {
        "username": ".+",
        "firstname": ".+",
        "lastname": ".+",
        "password": ".+",
    }

    sim_domain = ["[^']*' OR ''='"]

    def evaluate(self, selenium_mock, reg_individuals, sim_individuals):

        self.base = selenium_mock.base

        self.correction = 0

        payload = selenium_mock.payload

        # if selenium_mock.closest_page == '/users/home.php':

        if selenium_mock.closest_page == '/users/register.php':
            reg_individuals, best = regguess.main(
                target=payload,
                domain=self.reg_domain,
                population=reg_individuals
            )
            f = best.fitness.values[0]
            print("[Reg] {} >{}< {}".format(payload, f, best))

            self.correction = 1 / (1 + f)

        if selenium_mock.closest_page == '/users/similar.php':
            inner_individuals, best = stringguess.main(
                target=payload['firstname'],
                domain=self.sim_domain,
                population=sim_individuals
            )
            f = best.fitness.values[0]
            print("[SQLi] {} >{}< {}".format(payload, f, "".join(best)))

            self.correction = 1 / (1 + f)

        return reg_individuals, sim_individuals, self.base - self.correction
