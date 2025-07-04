import unittest
import numpy as np
import random
import sys
import os
import io
from functools import wraps
from unittest.mock import MagicMock
import sea_level as sea_level

current_directory = os.path.dirname(os.path.abspath(__file__))


# DO NOT MODIFY
def run_student_script(script_path, injected_globals):
    with open(script_path, "r") as f:
        student_code = f.read()

    # Capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # collect a log of all printed lines to distinguish from stack traces
    printed_lines = []

    class PrintLog:
        def write(self, text):
            printed_lines.append(text)

    def log_print(*args, **kwargs):
        # this line redirects to printed_lines var
        print(*args, **kwargs, file=PrintLog())
        # this one goes to stddout
        print(*args, **kwargs)

    locals = {}
    try:
        end_state = exec(student_code, {**injected_globals, "print": log_print}, locals)
    except Exception as e:
        print(f"Error: {e}")

    printed_lines = [line for line in printed_lines if line.strip()]

    sys.stdout = sys.__stdout__
    return (captured_output.getvalue().strip(), locals, printed_lines)


# DO NOT MODIFY
def case_options(points, failure, error):
    """Decorator to add points and messages to a test case"""

    def decorator(func):
        # Directly set attributes on the original function
        func.points = points
        func.failure_message = failure
        func.error_message = error

        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(args[-1], MagicMock):
                args = args[:-1]
            return func(*args, **kwargs)

        return wrapper

    return decorator


# DO NOT MODIFY
def testsuite_options(timeout, weight):
    """Decorator to add timeout and weight to a test suite"""

    def decorator(cls):
        # Directly set attributes on the original class
        cls.timeout = timeout
        cls.weight = weight

        return cls

    return decorator

class TestProblemSetBase(unittest.TestCase):
    """
    Base class for the test suite
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_script_path = None
        self.global_vars = {}

    def attempt_cases(self, inputs, expected, exact_match=False, exact_lines=False):
        """Attempt the test cases for a given task and checks for expected output"""

        injected_globals = self.global_vars.copy()
        injected_globals.update(inputs)

        output, student_vars, printed_lines = run_student_script(
            self.student_script_path, injected_globals
        )

        # lists of expected outputs
        if isinstance(expected, list):
            for expected_output in expected:
                if exact_match and expected_output != output:
                    self.fail(f"Expected {expected_output}, got {output}")
                elif (
                    not exact_match
                    and str(expected_output).lower() not in output.lower()
                ):
                    self.fail(f"Expected {expected_output}, got {output}")

        # tuple of expected outputs, in exact order
        elif isinstance(expected, tuple):

            if exact_lines and len(expected) != len(printed_lines):
                self.fail(f"Expected {len(expected)} outputs, got {len(printed_lines)}")

            for i, expected_output in enumerate(expected):
                if exact_match and expected_output != printed_lines[i]:
                    self.fail(f"Expected {expected_output}, got {printed_lines[i]}")
                elif (
                    not exact_match
                    and str(expected_output).lower() not in printed_lines[i].lower()
                ):
                    self.fail(f"Expected {expected_output}, got {printed_lines[i]}")

    def get_global_vars(self):
        """Return the global variables from the student script"""
        return self.global_vars


ANNUAL_SEA_LEVEL_DATA = np.array([[2030, 0.1700, 0.1500, 0.1900, 0.0100],
[2031, 0.1740, 0.1520, 0.1960, 0.0110],
[2032, 0.1780, 0.1540, 0.2020, 0.0120],
[2033, 0.1820, 0.1560, 0.2080, 0.0130],
[2034, 0.1860, 0.1580, 0.2140, 0.0140],
[2035, 0.1900, 0.1600, 0.2200, 0.0150],
[2036, 0.1940, 0.1620, 0.2260, 0.0160],
[2037, 0.1980, 0.1640, 0.2320, 0.0170],
[2038, 0.2020, 0.1660, 0.2380, 0.0180],
[2039, 0.2060, 0.1680, 0.2440, 0.0190],
[2040, 0.2100, 0.1700, 0.2500, 0.0200],
[2041, 0.2150, 0.1730, 0.2570, 0.0210],
[2042, 0.2200, 0.1760, 0.2640, 0.0220],
[2043, 0.2250, 0.1790, 0.2710, 0.0230],
[2044, 0.2300, 0.1820, 0.2780, 0.0240],
[2045, 0.2350, 0.1850, 0.2850, 0.0250],
[2046, 0.2400, 0.1880, 0.2920, 0.0260],
[2047, 0.2450, 0.1910, 0.2990, 0.0270],
[2048, 0.2500, 0.1940, 0.3060, 0.0280],
[2049, 0.2550, 0.1970, 0.3130, 0.0290],
[2050, 0.2600, 0.2000, 0.3200, 0.0300],
[2051, 0.2670, 0.2050, 0.3290, 0.0310],
[2052, 0.2740, 0.2100, 0.3380, 0.0320],
[2053, 0.2810, 0.2150, 0.3470, 0.0330],
[2054, 0.2880, 0.2200, 0.3560, 0.0340],
[2055, 0.2950, 0.2250, 0.3650, 0.0350],
[2056, 0.3020, 0.2300, 0.3740, 0.0360],
[2057, 0.3090, 0.2350, 0.3830, 0.0370],
[2058, 0.3160, 0.2400, 0.3920, 0.0380],
[2059, 0.3230, 0.2450, 0.4010, 0.0390],
[2060, 0.3300, 0.2500, 0.4100, 0.0400],
[2061, 0.3420, 0.2580, 0.4260, 0.0420],
[2062, 0.3540, 0.2660, 0.4420, 0.0440],
[2063, 0.3660, 0.2740, 0.4580, 0.0460],
[2064, 0.3780, 0.2820, 0.4740, 0.0480],
[2065, 0.3900, 0.2900, 0.4900, 0.0500],
[2066, 0.4020, 0.2980, 0.5060, 0.0520],
[2067, 0.4140, 0.3060, 0.5220, 0.0540],
[2068, 0.4260, 0.3140, 0.5380, 0.0560],
[2069, 0.4380, 0.3220, 0.5540, 0.0580],
[2070, 0.4500, 0.3300, 0.5700, 0.0600],
[2071, 0.4600, 0.3360, 0.5840, 0.0620],
[2072, 0.4700, 0.3420, 0.5980, 0.0640],
[2073, 0.4800, 0.3480, 0.6120, 0.0660],
[2074, 0.4900, 0.3540, 0.6260, 0.0680],
[2075, 0.5000, 0.3600, 0.6400, 0.0700],
[2076, 0.5100, 0.3660, 0.6540, 0.0720],
[2077, 0.5200, 0.3720, 0.6680, 0.0740],
[2078, 0.5300, 0.3780, 0.6820, 0.0760],
[2079, 0.5400, 0.3840, 0.6960, 0.0780],
[2080, 0.5500, 0.3900, 0.7100, 0.0800],
[2081, 0.5620, 0.3980, 0.7260, 0.0820],
[2082, 0.5740, 0.4060, 0.7420, 0.0840],
[2083, 0.5860, 0.4140, 0.7580, 0.0860],
[2084, 0.5980, 0.4220, 0.7740, 0.0880],
[2085, 0.6100, 0.4300, 0.7900, 0.0900],
[2086, 0.6220, 0.4380, 0.8060, 0.0920],
[2087, 0.6340, 0.4460, 0.8220, 0.0940],
[2088, 0.6460, 0.4540, 0.8380, 0.0960],
[2089, 0.6580, 0.4620, 0.8540, 0.0980],
[2090, 0.6700, 0.4700, 0.8700, 0.1000],
[2091, 0.6830, 0.4770, 0.8890, 0.1030],
[2092, 0.6960, 0.4840, 0.9080, 0.1060],
[2093, 0.7090, 0.4910, 0.9270, 0.1090],
[2094, 0.7220, 0.4980, 0.9460, 0.1120],
[2095, 0.7350, 0.5050, 0.9650, 0.1150],
[2096, 0.7480, 0.5120, 0.9840, 0.1180],
[2097, 0.7610, 0.5190, 1.0030, 0.1210],
[2098, 0.7740, 0.5260, 1.0220, 0.1240],
[2099, 0.7870, 0.5330, 1.0410, 0.1270],
[2100, 0.8000, 0.5400, 1.0600, 0.1300]])

CUMULATIVE_SEA_LEVEL_DATA = np.array([[2030, 0.17, -0.03,  0.37,  0.1],
 [2031, 0.344, 0.05417247, 0.63382753, 0.14491377],
 [2032, 0.522, 0.15868196, 0.88531804, 0.18165902],
 [2033, 0.704, 0.27504779, 1.13295221, 0.21447611],
 [2034, 0.89,  0.40010205, 1.37989795, 0.24494897],
 [2035, 1.08,  0.53227744, 1.62772256, 0.27386128],
 [2036, 1.274, 0.67067587, 1.87732413, 0.30166206],
 [2037, 1.472, 0.81473293, 2.12926707, 0.32863353],
 [2038, 1.674, 0.96407043, 2.38392957, 0.35496479],
 [2039, 1.88,  1.11842269, 2.64157731, 0.38078866],
 [2040, 2.09,  1.27759616, 2.90240384, 0.40620192],
 [2041, 2.305, 1.44244565, 3.16755435, 0.43127717],
 [2042, 2.525, 1.61285966, 3.43714034, 0.45607017],
 [2043, 2.75,  1.78875081, 3.71124919, 0.48062459],
 [2044, 2.98,  1.97004951, 3.98995049, 0.50497525],
 [2045, 3.215, 2.15669948, 4.27330052, 0.52915026],
 [2046, 3.455, 2.34865467, 4.56134533, 0.55317267],
 [2047, 3.7,   2.54587696, 4.85412304, 0.57706152],
 [2048, 3.95,  2.74833449, 5.15166551, 0.60083276],
 [2049, 4.205, 2.9560004,  5.4539996,  0.6244998 ],
 [2050, 4.465, 3.16885186, 5.76114814, 0.64807407],
 [2051, 4.732, 3.38886933, 6.07513067, 0.67156534],
 [2052, 5.006, 3.61603597, 6.39596403, 0.69498201],
 [2053, 5.287, 3.8503372,  6.7236628,  0.7183314 ],
 [2054, 5.575, 4.0917603,  7.0582397,  0.74161985],
 [2055, 5.87,  4.34029415, 7.39970585, 0.76485293],
 [2056, 6.172, 4.59592894, 7.74807106, 0.78803553],
 [2057, 6.481, 4.85865602, 8.10334398, 0.81117199],
 [2058, 6.797, 5.12846771, 8.46553229, 0.83426614],
 [2059, 7.12,  5.40535718, 8.83464282, 0.85732141],
 [2060, 7.45,  5.68931831, 9.21068169, 0.88034084],
 [2061, 7.792, 5.98423895, 9.59976105, 0.90388052],
 [2062, 8.146, 6.29019829, 10.00180171, 0.92790086],
 [2063, 8.512, 6.60726905, 10.41673095, 0.95236548],
 [2064, 8.89,  6.93551797, 10.84448203, 0.97724101],
 [2065, 9.28,  7.27500623, 11.28499377, 1.00249688],
 [2066, 9.682, 7.62578989, 11.73821011, 1.02810505],
 [2067, 10.096, 7.98792031, 12.20407969, 1.05403985],
 [2068, 10.522, 8.36144452, 12.68255548, 1.08027774],
 [2069, 10.96,  8.74640564, 13.17359436, 1.10679718],
 [2070, 11.41,  9.14284319, 13.67715681, 1.1335784 ],
 [2071, 11.87,  9.54879342, 14.19120658, 1.16060329],
 [2072, 12.34,  9.96428958, 14.71571042, 1.18785521],
 [2073, 12.82, 10.38936222, 15.25063778, 1.21531889],
 [2074, 13.31, 10.82403942, 15.79596058, 1.24298029],
 [2075, 13.81, 11.26834699, 16.35165301, 1.2708265 ],
 [2076, 14.32, 11.72230872, 16.91769128, 1.29884564],
 [2077, 14.84, 12.1859465, 17.4940535,  1.32702675],
 [2078, 15.37, 12.65928054, 18.08071946, 1.35535973],
 [2079, 15.91, 13.1423295, 18.6776705,  1.38383525],
 [2080, 16.46, 13.63511062, 19.28488938, 1.41244469],
 [2081, 17.022, 14.13963986, 19.90436014, 1.44118007],
 [2082, 17.596, 14.65593197, 20.53606803, 1.47003401],
 [2083, 18.182, 15.18400067, 21.17999933, 1.49899967],
 [2084, 18.78,  15.72385864, 21.83614136, 1.52807068],
 [2085, 19.39,  16.2755177, 22.5044823,  1.55724115],
 [2086, 20.012, 16.83898881, 23.18501119, 1.58650559],
 [2087, 20.646, 17.41428219, 23.87771781, 1.6158589 ],
 [2088, 21.292, 18.00140735, 24.58259265, 1.64529633],
 [2089, 21.95,  18.60037316, 25.29962684, 1.67481342],
 [2090, 22.62,  19.21118789, 26.02881211, 1.70440605],
 [2091, 23.303, 19.83428266, 26.77171734, 1.73435867],
 [2092, 23.999, 20.46969412, 27.52830588, 1.76465294],
 [2093, 24.708, 21.11745687, 28.29854313, 1.79527157],
 [2094, 25.43,  21.77760353, 29.08239647, 1.82619824],
 [2095, 26.165, 22.45016488, 29.87983512, 1.85741756],
 [2096, 26.913, 23.13516994, 30.69083006, 1.88891503],
 [2097, 27.674, 23.83264607, 31.51535393, 1.92067696],
 [2098, 28.448, 24.5426191, 32.3533809,  1.95269045],
 [2099, 29.235, 25.26511335, 33.20488665, 1.98494332],
 [2100, 30.035, 26.0001518, 34.0698482, 2.0174241 ]])

# ########### PART 1 ###########
@testsuite_options(4, 1)
class TestProblemSetPart1(TestProblemSetBase):
    """
    Test suite for Part 1 of Problem Set 2
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_vars = {}

    @case_options(
        2.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_predict_sea_level_rise(self):
        student_out =  sea_level.predict_sea_level_rise()
        expected_out = ANNUAL_SEA_LEVEL_DATA.copy()
        epsilon = 1e-1

        self.assertIsNotNone(student_out, " predict_sea_level_rise() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f" predict_sea_level_rise() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertEqual(expected_out.shape[0], student_out.shape[0], f" predict_sea_level_rise() returned incorrect number of rows. Expected: {len(expected_out)} Got: {student_out.shape[0]}")
        self.assertEqual(expected_out.shape[1], student_out.shape[1], f" predict_sea_level_rise() returned incorrect number of columns. Expected: {len(expected_out[0])} Got: {student_out.shape[1]}")
        for row in expected_out:
            year = row[0]
            student_row = None
            for r in student_out:
                if r[0] == year:
                    student_row = r
                    break
            self.assertIsNotNone(student_row, f" predict_sea_level_rise() is missing data for year {year}")
            self.assertAlmostEqual(row[1], student_row[1], delta=epsilon, msg=f"For year {year}, expected mean of {row[1]} but got mean of {student_row[1]}")
            self.assertAlmostEqual(row[2], student_row[2], delta=epsilon, msg=f"For year {year}, expected lower 25% of {row[2]} but got lower 25% of {student_row[2]}")
            self.assertAlmostEqual(row[3], student_row[3], delta=epsilon, msg=f"For year {year}, expected upper 25% of {row[3]} but got upper 25% of {student_row[3]}")
            self.assertAlmostEqual(row[4], student_row[4], delta=epsilon, msg=f"For year {year}, expected std_dev of {row[4]} but got std_dev of {student_row[4]}")
    @case_options(
        1.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_cumulative_sea_level_rise(self):
        student_out =  sea_level.predict_cumulative_sea_level_rise(False)
        expected_out = CUMULATIVE_SEA_LEVEL_DATA.copy()
        epsilon = 1e-1

        self.assertIsNotNone(student_out, " predict_cumulative_sea_level_rise() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f" predict_cumulative_sea_level_rise() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertEqual(expected_out.shape[0], student_out.shape[0], f" predict_cumulative_sea_level_rise() returned incorrect number of rows. Expected: {len(expected_out)} Got: {student_out.shape[0]}")
        self.assertEqual(expected_out.shape[1], student_out.shape[1], f" predict_cumulative_sea_level_rise() returned incorrect number of columns. Expected: {len(expected_out[0])} Got: {student_out.shape[1]}")
        for row in expected_out:
            year = row[0]
            student_row = None
            for r in student_out:
                if r[0] == year:
                    student_row = r
                    break
            self.assertIsNotNone(student_row, f" predict_cumulative_sea_level_rise() is missing data for year {year}")
            self.assertAlmostEqual(row[1], student_row[1], delta=epsilon, msg=f"For year {year}, expected mean of {row[1]} but got mean of {student_row[1]}")
            self.assertAlmostEqual(row[2], student_row[2], delta=epsilon, msg=f"For year {year}, expected lower 25% of {row[2]} but got lower 25% of {student_row[2]}")
            self.assertAlmostEqual(row[3], student_row[3], delta=epsilon, msg=f"For year {year}, expected upper 25% of {row[3]} but got upper 25% of {student_row[3]}")
            self.assertAlmostEqual(row[4], student_row[4], delta=epsilon, msg=f"For year {year}, expected std_dev of {row[4]} but got std_dev of {student_row[4]}")


    @case_options(
        1.0,
        "Your code does not have the correct simulated values",
        "Your code throws an error when simulating a year",
    )
    def test_simulate_year(self):
        #tests simulate_year for N=1

        NUM_TRIALS = 10000
        YEAR = 2073
        N = 1

        epsilon = 1e-1

        student_out = sea_level.simulate_year(ANNUAL_SEA_LEVEL_DATA, YEAR, N)

        self.assertIsNotNone(student_out, "simulate_year() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f"simulate_year() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertTrue(len(student_out.shape)==1, f"Expected simulate_year() to return a 1 dimensional numpy array. Got numpy array of shape {student_out.shape}")
        self.assertEqual(N, student_out.shape[0], f"Expected simulate_year() to return 1-D numpy array with {N} elements. Got {student_out.shape[0]}")

        student_outputs = []
        for _ in range(NUM_TRIALS):
            student_outputs.append(sea_level.simulate_year(ANNUAL_SEA_LEVEL_DATA, YEAR, N))

        student_mean = np.mean(np.array(student_outputs))
        student_std = np.std(np.array(student_outputs))

        expected_mean = ANNUAL_SEA_LEVEL_DATA[YEAR-2030][1]
        expected_std = ANNUAL_SEA_LEVEL_DATA[YEAR-2030][4]

        self.assertAlmostEqual(expected_mean, student_mean, delta=epsilon, msg=f"For year {YEAR}, expected simulate_year() to return outputs with mean {expected_mean}. Got {student_mean}")
        self.assertAlmostEqual(expected_std, student_std, delta=epsilon, msg=f"For year {YEAR}, expected simulate_year() to return outputs with std_dev {expected_std}. Got {student_std}")


@testsuite_options(4, 1)
class TestProblemSetPart2(TestProblemSetBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.global_vars = {}


    @case_options(
        1.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_simulate_water_levels(self):
        np.random.seed(0)
        random.seed(0)
        expected_output = [0.18764052345967666, 0.17840172929203946, 0.18974485580926886, 0.21113161158961893, 0.21214581186209955, 0.17534083180185384, 0.20920141468040943, 0.19542692745893914, 0.20014206066771598, 0.21380137153682907, 0.21288087142321754, 0.24553974364622247, 0.23674282995323387, 0.22779852537933507, 0.2406527175858902, 0.24334185818435666, 0.27884605590209777, 0.23946072687832337, 0.25876589564622526, 0.23023122356025, 0.18341030552497767, 0.2872621764586512, 0.3016619583635042, 0.2565085543265874, 0.36517165721557865, 0.24409720138904323, 0.30364730662285205, 0.30207419754904413, 0.3742456101456214, 0.3803049920261111, 0.33619789702787667, 0.35788282582329134, 0.314937427104275, 0.27488336246169937, 0.3613002168323447, 0.397817448455199, 0.46597511539784153, 0.4789285118343582, 0.40430969822515467, 0.4204664404666305, 0.38708682209597445, 0.37195888789490356, 0.3607987077999992, 0.6087511760852982, 0.4553436516408875, 0.46933479888721696, 0.41979873407640533, 0.5775342863315613, 0.4073437635855957, 0.5234062581433104, 0.478362675104506, 0.5937260048244596, 0.5310923684442146, 0.48446563216547256, 0.5955199639061983, 0.6485498683477375, 0.6281195844592514, 0.6624323583875394, 0.5851050790066276, 0.6224513657332605, 0.6027539552224049, 0.6459660243613243, 0.6098064941032878, 0.5208351963458472, 0.7418717279324203, 0.6887951923360499, 0.5556365950580068, 0.8169966529186187, 0.661495002816478, 0.7935970652661097, 0.8947817730830798]
        student_output = sea_level.simulate_water_levels(ANNUAL_SEA_LEVEL_DATA)

        self.assertIsNotNone(student_output, "simulate_water_levels() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected simulate_water_levels() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected simulate_water_levels() to return list of length {len(expected_output)}. Got {len(student_output)}")

        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For simulate_water_levels(), for year {2030+i}, expected water level of {expected_output[i]}. Got {student_output[i]}")

    @case_options(
        1.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_no_insurance_costs(self):
        np.random.seed(0)
        random.seed(0)

        annual_rises = [0.18764052345967666, 0.17840172929203946, 0.18974485580926886, 0.21113161158961893, 0.21214581186209955, 0.17534083180185384, 0.20920141468040943, 0.19542692745893914, 0.20014206066771598, 0.21380137153682907, 0.21288087142321754, 0.24553974364622247, 0.23674282995323387, 0.22779852537933507, 0.2406527175858902, 0.24334185818435666, 0.27884605590209777, 0.23946072687832337, 0.25876589564622526, 0.23023122356025, 0.18341030552497767, 0.2872621764586512, 0.3016619583635042, 0.2565085543265874, 0.36517165721557865, 0.24409720138904323, 0.30364730662285205, 0.30207419754904413, 0.3742456101456214, 0.3803049920261111, 0.33619789702787667, 0.35788282582329134, 0.314937427104275, 0.27488336246169937, 0.3613002168323447, 0.397817448455199, 0.46597511539784153, 0.4789285118343582, 0.40430969822515467, 0.4204664404666305, 0.38708682209597445, 0.37195888789490356, 0.3607987077999992, 0.6087511760852982, 0.4553436516408875, 0.46933479888721696, 0.41979873407640533, 0.5775342863315613, 0.4073437635855957, 0.5234062581433104, 0.478362675104506, 0.5937260048244596, 0.5310923684442146, 0.48446563216547256, 0.5955199639061983, 0.6485498683477375, 0.6281195844592514, 0.6624323583875394, 0.5851050790066276, 0.6224513657332605, 0.6027539552224049, 0.6459660243613243, 0.6098064941032878, 0.5208351963458472, 0.7418717279324203, 0.6887951923360499, 0.5556365950580068, 0.8169966529186187, 0.661495002816478, 0.7935970652661097, 0.8947817730830798]
        expected_output = [0.01752810469193533, 0.03320845055034322, 0.05115742171219699, 0.07449690518908267, 0.09814064874771253, 0.1132088151080833, 0.13596923951220613, 0.15505462500399395, 0.17509724320430872, 0.19923765466535745, 0.22310191609232272, 0.25676383918618945, 0.2877866881721596, 0.3161262457859601, 0.34832206106172714, 0.38132461851703414, 0.4249784352876635, 0.4568166533511605, 0.4944464220450281, 0.523515789113103, 0.5401978502180985, 0.5863765031556939, 0.6368750906647451, 0.6738276569627214, 0.743379154127395, 0.776608314544108, 0.8277025065309636, 0.8783247657956768, 0.9505984488393632, 1.0246899464471966, 1.0855493155555596, 1.152914163302547, 1.2073953914338296, 1.2498604001723395, 1.3182504652220428, 1.3975956997586025, 1.497388234377955, 1.6010667879282625, 1.6823596973958088, 1.768499629535798, 1.8446256761645903, 1.9162133425330614, 1.9844529548730612, 2.1388285429157103, 2.2354316384079764, 2.3362320780741417, 2.4221716982970634, 2.563185412829688, 2.645388541905367, 2.764751045162691, 2.8682598476940426, 3.0157502496238267, 3.1381871970015123, 3.243526886651154, 3.3917348722136333, 3.5660098063875023, 3.730069598617128, 3.911285777810898, 4.055327809413549, 4.216553492280179, 4.367930469891381, 4.540913482072043, 4.695816729123687, 4.814150807662026, 5.035086671628236, 5.229484267796261, 5.361738905819464, 5.611738905819464, 5.7924864072277025, 6.0392849398607575, 6.2892849398607575]

        student_output = sea_level.no_insurance_costs(annual_rises)

        self.assertIsNotNone(student_output, "no_insurance_costs() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected no_insurance_costs() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected no_insurance_costs() to return list of length {len(expected_output)}. Got {len(student_output)}")

        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For no_insurance_costs(), for year {2020+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")


    @case_options(
        1.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_insure_immediately_costs(self):
        np.random.seed(0)
        random.seed(0)

        annual_rises = [0.18764052345967666, 0.17840172929203946, 0.18974485580926886, 0.21113161158961893, 0.21214581186209955, 0.17534083180185384, 0.20920141468040943, 0.19542692745893914, 0.20014206066771598, 0.21380137153682907, 0.21288087142321754, 0.24553974364622247, 0.23674282995323387, 0.22779852537933507, 0.2406527175858902, 0.24334185818435666, 0.27884605590209777, 0.23946072687832337, 0.25876589564622526, 0.23023122356025, 0.18341030552497767, 0.2872621764586512, 0.3016619583635042, 0.2565085543265874, 0.36517165721557865, 0.24409720138904323, 0.30364730662285205, 0.30207419754904413, 0.3742456101456214, 0.3803049920261111, 0.33619789702787667, 0.35788282582329134, 0.314937427104275, 0.27488336246169937, 0.3613002168323447, 0.397817448455199, 0.46597511539784153, 0.4789285118343582, 0.40430969822515467, 0.4204664404666305, 0.38708682209597445, 0.37195888789490356, 0.3607987077999992, 0.6087511760852982, 0.4553436516408875, 0.46933479888721696, 0.41979873407640533, 0.5775342863315613, 0.4073437635855957, 0.5234062581433104, 0.478362675104506, 0.5937260048244596, 0.5310923684442146, 0.48446563216547256, 0.5955199639061983, 0.6485498683477375, 0.6281195844592514, 0.6624323583875394, 0.5851050790066276, 0.6224513657332605, 0.6027539552224049, 0.6459660243613243, 0.6098064941032878, 0.5208351963458472, 0.7418717279324203, 0.6887951923360499, 0.5556365950580068, 0.8169966529186187, 0.661495002816478, 0.7935970652661097, 0.8947817730830798]
        expected_output = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.20033239167270084, 0.20033239167270084, 0.21336672311581656, 0.21336672311581656, 0.21409618444038697, 0.2145110239501958, 0.22936014597932008, 0.2454211443845423, 0.2526607237901176, 0.2642372889547759, 0.2672247743756309, 0.2672247743756309, 0.2794848177420999, 0.2990483074331397, 0.33884084205249215, 0.38251939560279963, 0.40381230507034604, 0.4299522372103352, 0.4473696016295301, 0.4617613792085108, 0.4739211207685106, 0.5565464735941, 0.5931495690863663, 0.6339500087525314, 0.659889628975453, 0.7331499148749214, 0.7553530439506001, 0.8123749213935932, 0.855883723924945, 0.9340015253722829, 0.9933292359055472, 1.038668925555189, 1.1173249147270485, 1.2118898752313698, 1.3003257505691452, 1.399055458085407, 1.4745869817873953, 1.5613223915073735, 1.642148578074095, 1.7359383853824923, 1.8188803336134787, 1.8751308925172328, 2.001879583690201, 2.108518141391016, 2.175209119908418, 2.325209119908418, 2.4236576207533616, 2.5710964468598054, 2.7210964468598053]

        student_output = sea_level.insure_immediately_costs(annual_rises)

        self.assertIsNotNone(student_output, "insure_immediately_costs() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected insure_immediately_costs() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected insure_immediately_costs() to return list of length {len(expected_output)}. Got {len(student_output)}")

        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For insure_immediately_costs(), for year {2020+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")

    @case_options(
        1.0,
        "Your code does not have the correct values for the output array",
        "Your code throws an error when creating the output array",
    )
    def test_invest_and_wait_a_bit_costs(self):
        np.random.seed(0)
        random.seed(0)

        annual_rises = [0.18764052345967666, 0.17840172929203946, 0.18974485580926886, 0.21113161158961893, 0.21214581186209955, 0.17534083180185384, 0.20920141468040943, 0.19542692745893914, 0.20014206066771598, 0.21380137153682907, 0.21288087142321754, 0.24553974364622247, 0.23674282995323387, 0.22779852537933507, 0.2406527175858902, 0.24334185818435666, 0.27884605590209777, 0.23946072687832337, 0.25876589564622526, 0.23023122356025, 0.18341030552497767, 0.2872621764586512, 0.3016619583635042, 0.2565085543265874, 0.36517165721557865, 0.24409720138904323, 0.30364730662285205, 0.30207419754904413, 0.3742456101456214, 0.3803049920261111, 0.33619789702787667, 0.35788282582329134, 0.314937427104275, 0.27488336246169937, 0.3613002168323447, 0.397817448455199, 0.46597511539784153, 0.4789285118343582, 0.40430969822515467, 0.4204664404666305, 0.38708682209597445, 0.37195888789490356, 0.3607987077999992, 0.6087511760852982, 0.4553436516408875, 0.46933479888721696, 0.41979873407640533, 0.5775342863315613, 0.4073437635855957, 0.5234062581433104, 0.478362675104506, 0.5937260048244596, 0.5310923684442146, 0.48446563216547256, 0.5955199639061983, 0.6485498683477375, 0.6281195844592514, 0.6624323583875394, 0.5851050790066276, 0.6224513657332605, 0.6027539552224049, 0.6459660243613243, 0.6098064941032878, 0.5208351963458472, 0.7418717279324203, 0.6887951923360499, 0.5556365950580068, 0.8169966529186187, 0.661495002816478, 0.7935970652661097, 0.8947817730830798]
        expected_output = [0.006728104691935331, 0.011025250550343224, 0.016976328912197004, 0.027670033377882687, 0.03798512585870775, 0.03900489398307226, 0.04695830664644449, 0.05043710176348119, 0.05403037370880829, 0.06083317421709998, 0.06642359369985934, 0.08082488738453306, 0.09154703297321376, 0.09848964920627121, 0.10813308826673507, 0.11736544119111249, 0.13596546238614204, 0.14139697991295688, 0.15119408624116148, 0.15092782717582767, 0.13669013833621033, 0.15027937483218373, 0.16642871741176546, 0.1671771795540808, 0.1985695509386878, 0.1915789927832106, 0.4002816013949778, 0.4006964409047866, 0.41554556293391093, 0.43160656133913317, 0.4388461407447085, 0.4504227059093668, 0.4534101913302218, 0.4534101913302218, 0.4656702346966908, 0.4852337243877306, 0.5250262590070831, 0.5687048125573906, 0.5899977220249369, 0.616137654164926, 0.6335550185841209, 0.6479467961631016, 0.6601065377231015, 0.7427318905486909, 0.7793349860409572, 0.8201354257071223, 0.8460750459300439, 0.9193353318295123, 0.941538460905191, 0.9985603383481841, 1.042069140879536, 1.1201869423268738, 1.1795146528601381, 1.22485434250978, 1.3035103316816394, 1.3980752921859607, 1.4865111675237361, 1.585240875039998, 1.6607723987419862, 1.7475078084619644, 1.8283339950286859, 1.9221238023370832, 2.0050657505680696, 2.061316309471824, 2.188065000644792, 2.2947035583456072, 2.3613945368630094, 2.5113945368630093, 2.609843037707953, 2.7572818638143968, 2.9072818638143967]
        student_output = sea_level.invest_and_wait_a_bit_costs(annual_rises)

        self.assertIsNotNone(student_output, "invest_and_wait_a_bit_costs() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected invest_and_wait_a_bit_costs() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected invest_and_wait_a_bit_costs() to return list of length {len(expected_output)}. Got {len(student_output)}")

        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For invest_and_wait_a_bit_costs(), for year {2030+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")

class Results_600(unittest.TextTestResult):
    """
    Custom test result class to capture output and points
    """
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 0
        self.max_points = 0

    def addSuccess(self, test):
        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        self.points += pts
        self.max_points += pts

        return super().addSuccess(test)

    def addFailure(self, test, err):

        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        failure_message = getattr(func, "failure_message", "")

        self.output.append(f"❌ [-{pts}] {failure_message}, {err[1]}\n")
        self.max_points += pts

        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        method = getattr(test, getattr(test, "_testMethodName"))
        func = method.__func__
        pts = getattr(func, "points", 0)

        error_message = getattr(func, "error_message", "")

        self.output.append(f"❌ [-{pts}] {error_message}, {err[1]}\n")
        self.max_points += pts

        super(Results_600, self).addError(test, err)

    def getOutput(self):
        """
        Return the captured output
        """
        if self.points > 0:
            self.output.append(
                f"\n✅ [+{self.points}] {self.points == self.max_points and 'All' or 'Other'} tests passed!\n"
            )

        return "\n".join(self.output)

    def getPoints(self):
        """
        Return the total points
        """

        return self.points


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPart1))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProblemSetPart2))

    runner = unittest.TextTestRunner(resultclass=Results_600, verbosity=2)
    result = runner.run(suite)

    output = result.getOutput()
    points_earned = round(result.getPoints(), 3)

    print(output)

    print(f"Total points: {points_earned} / {result.max_points}")
