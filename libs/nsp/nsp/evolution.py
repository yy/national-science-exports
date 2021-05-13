"""National evolution of scientific profile based on the model.
"""
import numpy as np
import pandas as pd


class EvolutionModel:
    def __init__(self, density_file, params_file, income_group=False):
        """Initialize the model.

        Parameters
        ----------
        density_file: a path to a dataframe
            The dataframe contains, for each country and current time period,
            discipline, density around the discipline, state of the discipline
            at the period and that in the next time period.

        params_file : a path to a dataframe
            The dataframe contains the CONSTANT and SLOPE of the linear
            regression results from data, organized by INCOME_GROUP ["L", "LM",
            "UM", "H", "ALL"] as well as the START_STATE (0: disadv, 1: adv).

        income_group : a boolean flag
            This parameter sets whether the null model will be calculated with
            the regression coefficients from the income group-baesd results or
            aggregated one. Currently only the aggregated version is
            implemented.
        """
        self.ddf = pd.read_csv(density_file)
        self.params = self.load_params(pd.read_csv(params_file))
        self.countries = set(self.ddf.COUNTRY)
        self.disciplines = set(self.ddf.DIS)
        self.periods = sorted(self.ddf.CRRT_TIME.unique())

        # whether to use income group based params or not. not implemented for
        # self.income_group == True
        self.income_group = income_group

    def calculate_prob(self):
        """Convert the density values to the probability weight values."""

        def dens_to_prob(density, constant, slope):
            return constant + density * slope

        dis2adv_params = self.params[("ALL", 0)]
        adv2dis_params = self.params[("ALL", 1)]
        self.ddf["PROB"] = self.ddf.apply(
            lambda x: dens_to_prob(
                x["Density"], dis2adv_params["CONSTANT"], dis2adv_params["SLOPE"]
            )
            if x["st0"] == 0
            else dens_to_prob(
                x["Density"], adv2dis_params["CONSTANT"], adv2dis_params["SLOPE"]
            ),
            axis=1,
        )

    def sample(self, country, period):
        """Sample the RCA profile in the next time step for a country.

        We first count the number of new advantages (:num_new_advs:) and new
        disadvantages (:num_new_disadvs:) that the country actually had in the
        data.

        Then, based on the current density, we sample the :num_new_advs: newly
        activated disciplines and :num_new_disadvs: newly deactivated
        disciplines.
        """
        if "PROB" not in self.ddf.columns:
            self.calculate_prob()
        df = self.ddf.query(f"COUNTRY == '{country}' & CRRT_TIME == '{period}'")

        num_new_advs = len(df.query("st0 == 0 & st1 == 1"))
        num_new_disadvs = len(df.query("st0 == 1 & st1 == 0"))

        curr_advs = df.query("st0 == 1")
        curr_disadvs = df.query("st1 == 0")

        p_adv = curr_disadvs["PROB"] / sum(curr_disadvs["PROB"])
        p_disadv = curr_advs["PROB"] / sum(curr_advs["PROB"])

        new_advs = np.random.choice(
            curr_disadvs.DIS, num_new_advs, replace=False, p=p_adv
        )
        new_disadvs = np.random.choice(
            curr_advs.DIS, num_new_disadvs, replace=False, p=p_disadv
        )

        return num_new_advs, new_advs, num_new_disadvs, new_disadvs

    def load_params(self, params_df):
        """turns the parameter dataframe into a dictionary like the following:

        {('L', 0): {'CONSTANT': -0.06769076610324262, 'SLOPE': 0.8742293118684075},
         ('L', 1): {'CONSTANT': 0.8080063254977606, 'SLOPE': -1.3042906983151927},
         ...
        }
        """
        return params_df.set_index(["INCOME_GROUP", "START_STATE"]).to_dict(
            orient="index"
        )
