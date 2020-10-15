'''
Filename: symbolic_regression.py
Project: cyGOURGS - global optimization by uniform random global search using 
         cython code


This code runs the symbolic regression against a specified CSV dataset. Results 
of the run are housed in a HallOfFame class (copied from the DEAP project, 
https://github.com/DEAP/deap/blob/master/deap/tools/support.py, copyright
remains that of the respective authors), and the HallOfFame is saved in a user
specified database file.
         
Copyright Sohrab Towfighi 2020.
Razvan Tarnovan is a C/C++ developer who contributed a great deal to this 
project in porting it from Python to C++/Cython.

Released under GPL v 3.0 licence.

Usage can be found by running `python3 symbolic_regression.py -h`
'''

import sys
import csv
import copy
import random
import numpy as np
import pdb
import datetime
from functools import partial
import multiprocessing as mp
import pandas
import parmap
import tqdm
import lmfit
import sys,os
import sympy
from math_funcs import *
from sympy import simplify, sympify, Symbol
import time
import argparse 
from sqlitedict import SqliteDict
from support import HallOfFame
sys.path.append(os.path.join('.', '..', '..'))
import cython_call as cy
start_time = time.time()

fitting_param_prefix = 'params["p'
fitting_param_suffix = '"]'
variable_prefix = ''#'begin_v_'
variable_suffix = ''#'_end_v'


def has_nans(X):
    if np.any(np.isnan(X)):
        return True
    else:
        return False


def check_for_nans(X):
    if has_nans(X):
        raise Exception("Has NaNs")


def make_parameter_name(par):
    """
    Converts a fitting parameter name to pySRURGS safe parameter name. Prevents
    string manipulations on parameter names from affecting function names.

    Parameters
    ----------
    par : string
        A variable name.

    Returns
    -------
    par_name: string
        `par` wrapped in the pySRURGS parameter prefix and suffix.
    """
    par_name = fitting_param_prefix + str(par) + fitting_param_suffix
    return par_name
    

def create_parameter_list(m):
    """
    Creates a list of all the fitting parameter names.

    Parameters
    ----------
    m : int
        The number of fitting parameters in the symbolic regression problem

    Returns
    -------
    my_pars: list
        A list with fitting parameter names as elements.
    """
    my_pars = []
    for i in range(0, m):
        my_pars.append(make_parameter_name(str(i)))
    return my_pars


def create_fitting_lmfit_parameters(max_params, param_values=None):
    """
    Creates the lmfit.Parameters object based on the number of fitting 
    parameters permitted in this symbolic regression problem.

    Parameters
    ----------
    max_params: int
        The maximum number of fitting parameters. Same as `max_num_fit_params`.

    param_values: None OR (numpy.array of length max_params)
        Specifies the values of the fitting parameters. If none, will default
        to an array of ones, which are to be optimized later.

    Returns
    -------
    params: lmfit.Parameters
        Fitting parameter names specified as ['p' + str(integer) for integer
        in range(0, max_params)]
    """
    params = lmfit.Parameters()
    for int_param in range(0, max_params):
        param_name = 'p' + str(int_param)
        param_init_value = np.float(1)
        params.add(param_name, param_init_value)
    if param_values is not None:
        for int_param in range(0, max_params):
            param_name = 'p' + str(int_param)
            params[param_name].value = param_values[int_param]
    return params
    
    
def make_variable_name(var):
    """
    Converts a variable name to pySRURGS safe variable names. Prevents string
    manipulations on variable names from affecting function names.

    Parameters
    ----------
    var : string
        A variable name.

    Returns
    -------
    var_name: string
        `var` wrapped in the pySRURGS variable prefix and suffix.
    """
    var_name = variable_prefix + str(var) + variable_suffix
    return var_name
    

def create_variable_list(m):
    """
    Creates a list of all the variable names.

    Parameters
    ----------
    m : string (1) or int (2)
        (1) Absolute or relative path to a CSV file with a header
        (2) The number of independent variables in the dataset

    Returns
    -------
    my_vars: list
        A list with dataset variable names as elements.
    """
    if type(m) == str:
        my_vars = pandas.read_csv(m).keys()[:-1].tolist()
        my_vars = [make_variable_name(x) for x in my_vars]
    if type(m) == int:
        my_vars = []
        for i in range(0, m):
            my_vars.append(make_variable_name('x' + str(i)))
    return my_vars


def is_csv_valid(filepath, check_header=False):
    try:
        with open(filepath, 'r') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(2048))
    except Exception as e:
        print("Error encountering while reading: ", filepath)
        print(e)
        exit(2)
    if check_header == True:        
        with open(filepath, 'r') as csv_file:
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(csv_file.read(2048))
        if has_header == False:
            print("File which must have header is missing header: ", filepath)
            exit(2)


def check_validity_suggested_functions(suggested_funcs, arity):
    '''
    Takes a list of suggested functions to use in the search space and checks
    that they are valid.

    Parameters
    ----------
    suggested_funcs: list
        A list of strings.
        In case of `arity==1`, permitted values are ['sin','cos','tan','exp',
                                                     'log','tanh','sinh','cosh',
                                                     None]
        In case of `arity==2`, permitted values are ['add','sub','mul','div',
                                                     'pow', None]

    Returns
    -------
    suggested_funcs: list

    Raises
    ------
    Exception, if any of the suggested funcs is not in the permitted list
    '''
    valid_funcs_arity_1 = ['sin', 'cos', 'tan', 'exp', 'log', 'tanh', 'sinh', 
                           'cosh', None]
    valid_funcs_arity_2 = ['add', 'sub', 'mul', 'div', 'pow', None]
    if arity == 1:
        if suggested_funcs != [',']:
            for func in suggested_funcs:
                if func not in valid_funcs_arity_1:
                    msg = "Your suggested function of arity 1: " + func
                    msg += " is not in the list of valid functions"
                    msg += " " + str(valid_funcs_arity_1)
                    raise Exception(msg)
        else:
            suggested_funcs = []
    elif arity == 2:
        for func in suggested_funcs:
            if func not in valid_funcs_arity_2:
                msg = "Your suggested function of arity 2: " + func
                msg += " is not in the list of valid functions"
                msg += " " + str(valid_funcs_arity_2)
                raise Exception(msg)
    return suggested_funcs


class Result(object):
    def __init__(self, fitness, soln, simplified_soln):
        self.fitness = fitness
        self.soln = soln
        self.simplified_soln = simplified_soln
    def __eq__(self, other): 
        if not isinstance(other, Result):
            # don't attempt to compare against unrelated types
            raise NotImplementedError
        return self.simplified_soln == other.simplified_soln


def clean_all_parameter_names_for_sympy(equation_string, terminals):
    for terminal in terminals:
        if terminal.startswith('params'):
            amended_terminal = clean_parameter_name_for_sympy(terminal)
            equation_string = equation_string.replace(terminal, 
                                                      amended_terminal)
    return equation_string


def clean_parameter_name_for_sympy(parameter_name):
    amended_name = parameter_name.replace('["', '_')
    amended_name = amended_name.replace('"]', '')
    return amended_name
    

class Dataset(object):
    """
    A class used to store the dataset of the symbolic regression problem.

    Parameters
    ----------
    path_to_csv_file: string
       Absolute or relative path to the CSV file for the numerical data. The
       rightmost column of the CSV file should be the dependent variable.
       The CSV file should have a header of column names and should NOT
       have a leftmost index column.

    int_max_params: int
        The maximum number of fitting parameters specified in the symbolic
        regression problem.

    path_to_weights: string 
        An absolute or relative path to the CSV for weights of the data points 
        in the CSV found in `path_to_csv`. If `None`, will assume all data 
        points are equally weighted.

    Returns
    -------
    self
        A pyGOURGS.Dataset object, which houses a variety of attributes 
        including the numerical data, the sympy namespace, the data dict used in 
        evaluating the equation string, etc.
    """

    def __init__(self, 
                 path_to_csv_file, 
                 int_max_params, 
                 path_to_weights):
        (dataframe, header_labels) = self.load_csv_data(path_to_csv_file)
        if path_to_weights is not None:
            (weights_df, empty_labels) = self.load_csv_data(path_to_weights, 
                                                            header=None)            
            self._data_weights = np.squeeze(weights_df.values)
        else: 
            self._data_weights = None
        self._int_max_params = int_max_params
        self._dataframe = dataframe
        self._header_labels = header_labels
        x_data, x_labels = self.get_independent_data()
        y_data, y_label  = self.get_dependent_data()
        self._x_data = x_data
        self._x_labels = x_labels
        self._y_data = y_data
        self._y_label = y_label        
        if np.std(self._y_data) == 0:
            raise Exception("The data is invalid. All y values are the same.")
        self._param_names = [make_parameter_name(x) for x in
                             range(0, self._int_max_params)]
        self._data_dict = self.get_data_dict()
        self._num_variables = len(self._x_labels)
        self._num_terminals = self._num_variables + int_max_params
        self._terminals_list = (create_parameter_list(int_max_params) +
                                create_variable_list(path_to_csv_file))
        self._lmfit_params = create_fitting_lmfit_parameters(self._int_max_params)
        self._sympy_namespace = self.make_sympy_namespace()

    def make_sympy_namespace(self):
        sympy_namespace = {}
        for variable_name in self._x_labels:
            sympy_namespace[variable_name] = sympy.Symbol(variable_name)
        for param_name in self._param_names:
            amended_name = clean_parameter_name_for_sympy(param_name)
            sympy_namespace[amended_name] = sympy.Symbol(amended_name)
        sympy_namespace['add'] = sympy.Add
        sympy_namespace['sub'] = sympy_Sub
        sympy_namespace['mul'] = sympy.Mul
        sympy_namespace['div'] = sympy_Div
        sympy_namespace['pow'] = sympy.Pow
        sympy_namespace['cos'] = sympy.Function('cos')
        sympy_namespace['sin'] = sympy.Function('sin')
        sympy_namespace['tan'] = sympy.Function('tan')
        sympy_namespace['cosh'] = sympy.Function('cosh')
        sympy_namespace['sinh'] = sympy.Function('sinh')
        sympy_namespace['tanh'] = sympy.Function('tanh')
        sympy_namespace['exp'] = sympy.Function('exp')
        sympy_namespace['log'] = sympy.Function('log')
        return sympy_namespace
        
    def load_csv_data(self, path_to_csv, header=True):
        if header is True:
            dataframe = pandas.read_csv(path_to_csv)
        else:
            dataframe = pandas.read_csv(path_to_csv, header=header)
        column_labels = dataframe.keys()
        return (dataframe, column_labels)

    def get_independent_data(self):
        '''
            Loads all data in self._dataframe except the rightmost column
        '''
        dataframe = self._dataframe
        header_labels = self._header_labels
        features = dataframe.iloc[:, :-1]
        features = np.array(features)
        labels = header_labels[:-1]
        return (features, labels)

    def get_dependent_data(self):
        '''
            Loads only the rightmost column from self._dataframe
        '''
        dataframe = self._dataframe
        header_labels = self._header_labels
        feature = dataframe.iloc[:, -1]
        feature = np.array(feature)
        label = header_labels[-1]
        return (feature, label)

    def get_data_dict(self):
        '''
            Creates a dictionary object which houses the values in the dataset 
            CSV. The variable names in the CSV become keys in this data_dict 
            dictionary.
        '''
        dataframe = self._dataframe
        data_dict = dict()
        for label in self._header_labels:
            data_dict[label] = np.array(dataframe[label].values).astype(float)
            check_for_nans(data_dict[label])
        return data_dict


class SymbolicRegressionConfig(object):
    """
    An object used to store the configuration of this symbolic regression
    problem.

    Parameters
    ----------

    path_to_csv: string
        An absolute or relative path to the dataset CSV file. Usually, this
        file ends in a '.csv' extension.

    path_to_db: string
        An absolute or relative path to where the code can save an output
        database file. Usually, this file ends in a '.db' extension.

    n_functions: list
       A list with elements from the set ['add','sub','mul','div','pow'].
       Defines the functions of arity two that are permitted in this symbolic
       regression run. Default: ['add','sub','mul','div', 'pow']

    f_functions: list
        A list with elements from the set ['cos','sin','tan','cosh','sinh',
        'tanh','exp','log']. Defines the functions of arity one that are
        permitted in this symbolic regression run.
        Default: []

    max_num_fit_params: int
        This specifies the length of the fitting parameters vector. Randomly
        generated equations can have up to `max_num_fit_params` independent
        fitting parameters. Default: 3

    max_permitted_trees: int
        This specifies the number of permitted unique binary trees, which
        determine the structure of random equations. pyGOURGS will consider
        equations from [0 ... max_permitted_trees] during its search. Increasing
        this value increases the size of the search space. Default: 100

    path_to_weights: string 
        An absolute or relative path to the CSV for weights of the data points 
        in the CSV found in `path_to_csv`. If `None`, will assume all data 
        points are equally weighted.           
    
    Attributes
    ----------
    
    Most are simply the parameters which were passed in. Notably, there is the 
    dataset object, which is not a mere parameter.
    
    self._dataset
        A pyGOURGS.Dataset object, which houses a variety of attributes 
        including the numerical data, the sympy namespace, the data dict used in 
        evaluating the equation string, etc.
    
    Returns
    -------
    self
        A pyGOURGS.SymbolicRegressionConfig object, with attributes 
        self._path_to_csv, 
        self._path_to_db,
        self._n_functions, 
        self._f_functions, 
        self._max_num_fit_params, 
        self._max_permitted_trees,  
        self._path_to_weights, and 
        self._dataset.
    """

    def __init__(self,
                 path_to_csv,
                 path_to_db,
                 n_functions,
                 f_functions,
                 max_num_fit_params,
                 max_permitted_trees,
                 path_to_weights):  
        if path_to_db is None:
            path_to_db = create_db_name(path_to_csv)
        self._n_functions = n_functions
        self._f_functions = f_functions
        self._max_num_fit_params = max_num_fit_params
        self._max_permitted_trees = max_permitted_trees        
        self._path_to_csv = path_to_csv
        self._path_to_db = path_to_db
        is_csv_valid(path_to_csv, True)
        self._path_to_weights = path_to_weights
        if path_to_weights is not None:
            is_csv_valid(path_to_weights)
        self._dataset = Dataset(path_to_csv, 
                                max_num_fit_params, 
                                path_to_weights)


def compile(expr, variables):
    """Compile the expression *expr*.
    :param expr: Expression to compile. It can either be a PrimitiveTree,
                 a string of Python code or any object that when
                 converted into string produced a valid Python code
                 expression.
    :variables list: list of variable names
    :returns: a function if the primitive set has 1 or more arguments,
              or return the results produced by evaluating the tree.
    """
    code = str(expr)
    if len(variables) > 0:
        # This section is a stripped version of the lambdify
        # function of SymPy 0.6.6.
        args = 'params,' + ",".join(arg for arg in variables
                                    if not arg.startswith('params'))
        code = "lambda {args}: ({code})".format(args=args, code=code)
    try:
        return eval(code)
    except MemoryError:
        _, _, traceback = sys.exc_info()
        raise MemoryError("DEAP : Error in tree evaluation :"
                            " Python cannot evaluate a tree higher than 90. "
                            "To avoid this problem, you should use bloat control on your "
                            "operators. See the DEAP documentation for more information. "
                            "DEAP will now abort.", traceback)

                            
def evalSymbolicRegression(equation_string, SR_config, mode='residual'):
    """
        Evaluates the proposed solution according to its goodness of fit 
        measures.
    """
    # TODO need to add fitting parameters
    mydata = SR_config._dataset
    data_dict = mydata.get_data_dict() 
    independent_vars_vector, x_label = mydata.get_independent_data()
    dependent_var_vector, y_label = mydata.get_dependent_data()
    resid_lambda_func = compile(mydata._y_label + ' - ' + equation_string, mydata._terminals_list + [mydata._y_label])    
    lambda_func = compile(equation_string, mydata._terminals_list)    
    data_args = [mydata._data_dict[name] 
                 for name in mydata._terminals_list 
                 if not name.startswith('params')]
    data_args = data_args + [mydata._data_dict[mydata._y_label]]
    try: 
        try:
            minimizer_result = lmfit.minimize(resid_lambda_func, mydata._lmfit_params, 
                                              args=data_args, method='leastsq', 
                                              nan_policy='raise')
        except ValueError:
            return np.inf
    except TypeError:
        pdb.set_trace()
    mydata._lmfit_params = minimizer_result.params
    
    y_predicted = lambda_func(mydata._lmfit_params, *data_args[:-1])
    y_actual = dependent_var_vector
    if mode == 'residual':
        residual = y_actual - y_predicted

        if mydata._data_weights is not None:
            residual = np.multiply(residual, mydata._data_weights)            
        output = np.sum(residual**2)        
    elif mode == 'evaluate':
        output = y_predicted
    if np.size(output) == 1 and mode != 'residual':
        # if model only has parameters and no data variables, we can have a
        # situation where output is a single constant
        output = np.resize(output, np.size(independent_vars_vector))
    return output
    
    # TODO we need to ensure that fitting parameters are recognized and a suitable
    # nonlinear optimization package is used to find optimal values for these 
    # fitting parameters. We can try Levenburg-Marquardt algorithm via the LMFIT 
    # software https://lmfit.github.io/lmfit-py/ as was done in pySRURGS
    # raise Exception("fix this")


def simplify_equation_string(equation_string, dataset):
    equation_string = clean_all_parameter_names_for_sympy(equation_string, 
                                                        dataset._terminals_list)
    s = sympy.sympify(equation_string, locals=dataset._sympy_namespace)
    try:        
        equation_string = str(sympy.simplify(s))
    except ValueError:
        pass
    if 'zoo' in equation_string:  # zoo (complex infinity) in sympy
        return 'complex_infinity'
    # equation_string = remove_variable_tags(equation_string)
    # equation_string = remove_parameter_tags(equation_string)
    return equation_string


def solution_saving_worker(queue, n_items, hof):
    """
        Takes solutions from the queue of evaluated solutions, 
        then saves them to the hall of fame.
    """
    checkpoint = int(n_items/100) + 1
    for j in range(0, n_items):
        result = queue.get()
        hof.update([result])


def main_random(seed, enum, max_tree_complx, SR_config):
    """
        evaluates a randomly generated solution
    """
    soln = enum.uniform_random_global_search_once(max_tree_complx, seed=seed)
    simplified_soln = simplify_equation_string(soln, SR_config._dataset)
    score = evalSymbolicRegression(soln, SR_config)
    result = Result(score, soln, simplified_soln)
    return result


def main_random_queued(seed, enum, max_tree_complx, queue, SR_config):
    """
        evaluates a randomly generated solution
        and puts it in the queue 
        used for multiprocessing
    """
    soln = enum.uniform_random_global_search_once(max_tree_complx, seed=seed)
    simplified_soln = simplify_equation_string(soln, SR_config._dataset)
    score = evalSymbolicRegression(soln, SR_config)
    result = Result(score, soln, simplified_soln)    
    queue.put(result)


def main(soln, SR_config):
    """
        evaluates a proposed solution
    """
    score = evalSymbolicRegression(soln, SR_config)
    simplified_soln = simplify_equation_string(soln, SR_config._dataset)
    result = Result(score, soln, simplified_soln)    
    return result


def main_queued(soln, queue):
    """
        evaluates a proposed solution
        and puts the solution in the queue
        used for multiprocessing
    """
    score = evalSymbolicRegression(soln)    
    simplified_soln = simplify_equation_string(soln, SR_config._dataset)
    result = Result(score, soln, simplified_soln)    
    queue.put(result)


def str2bool(v):
    '''
        This helper function takes various ways of specifying True/False and 
        unifies them. Used in the command line interface.
    '''
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def create_seeds(start_time, n_iters):
    '''
        Creates a set of seeds between 0 and the max value of C long which is 
        system dependent
    '''
    if sys.maxsize > 2**32:
        bits = 64
    else:
        bits = 32
    if os.name == 'nt':
        LONG_MAX = 2**31
    elif os.name == 'posix' and bits == 64:
        LONG_MAX = 2**63
    elif os.name == 'posix' and bits == 32:
        LONG_MAX = 2**31
    else:
        raise Exception("Invalid os.name: only nt and posix are supported")
    a_time = float(start_time)
    seeds = np.arange(1, n_iters+1).astype(np.float)
    seeds = (seeds * a_time) % LONG_MAX
    if os.name == 'posix' and bits == 64:
        seeds = seeds.astype(np.int64).tolist()
    else:
        seeds = seeds.astype(np.int32).tolist()   
    return seeds


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='symbolic_regression.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("csv_path", help="An absolute filepath of the csv that houses your numerical data. Must have a header row of variable names.")
    parser.add_argument("-weights_path", help="An absolute filepath of the csv that will contain the relative weights of the datapoints.")
    parser.add_argument("-funcs_arity_two", help="a comma separated string listing the functions of arity two you want to be considered. Permitted:add,sub,mul,div,pow", default='add,sub,mul,div,pow')
    parser.add_argument("-funcs_arity_one", help="a comma separated string listing the functions of arity one you want to be considered. Permitted:sin,cos,tan,exp,log,sinh,cosh,tanh")
    parser.add_argument("-num_trees", help="pyGOURGS iterates through all the possible trees using an enumeration scheme. This argument specifies the number of trees to which we restrict our search.", type=int, default=1000)
    parser.add_argument("-num_iters", help="An integer specifying the number of solutions to be attempted in this run", type=int, default=100)
    parser.add_argument("-hall_of_fame_size", help="An integer specifying the number of solutions to be housed in this run", type=int, default=100)
    parser.add_argument("-max_num_fit_params", help="the maximum number of fitting parameters permitted in the generated models", default=3, type=int)
    parser.add_argument("-freq_print", help="An integer specifying how many strategies should be attempted before printing current job status", type=int, default=10)
    parser.add_argument("-deterministic", help="should algorithm be run in deterministic manner?", type=str2bool, default=False)
    parser.add_argument("-exhaustive", help="should algorithm be run in exhaustive/brute-force mode? This can run forever if you are not careful.", type=str2bool, default=False)
    parser.add_argument("-multiprocessing", help="should algorithm be run in multiprocessing mode?", type=str2bool, default=False)
    parser.add_argument("output_db", help="An absolute filepath where we save the hall of fame. Include the filename. Extension is typically '.db'")
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    arguments = parser.parse_args()   
    csv_path = arguments.csv_path
    weights_path = arguments.weights_path
    maximum_tree_complexity_index = arguments.num_trees
    n_iters = arguments.num_iters
    max_num_fit_params = arguments.max_num_fit_params
    frequency_printing = arguments.freq_print
    deterministic = arguments.deterministic
    exhaustive = arguments.exhaustive
    multiproc = arguments.multiprocessing
    output_db = arguments.output_db
    n_funcs = arguments.funcs_arity_two
    n_funcs = n_funcs.split(',')
    n_funcs = check_validity_suggested_functions(n_funcs, 2)
    f_funcs = arguments.funcs_arity_one
    if f_funcs is None or f_funcs == '':
        f_funcs = []
    else:
        f_funcs = f_funcs.split(',')
        f_funcs = check_validity_suggested_functions(f_funcs, 1)
    SR_config = SymbolicRegressionConfig(csv_path, 
                                        output_db, 
                                        n_funcs, 
                                        f_funcs, 
                                        max_num_fit_params, 
                                        maximum_tree_complexity_index, 
                                        weights_path)
    pset = cy.CyPrimitiveSet()    
    for operator_arity_2 in n_funcs:        
        pset.add_operator(operator_arity_2, 2)
    for operator_arity_1 in f_funcs:        
        pset.add_operator(operator_arity_1, 1)
    for terminal in SR_config._dataset._terminals_list:
        pset.add_variable(terminal)
    enum = cy.CyEnumerator(pset)
    if deterministic == False:
        deterministic = None
    best_score = np.inf
    iter = 0
    manager = mp.Manager()
    queue = manager.Queue()
    hof = HallOfFame(maxsize=100)
    if exhaustive == True:
        _, weights = enum.calculate_Q(maximum_tree_complexity_index)
        num_solns = int(numpy.sum(weights))
        txt = input("The number of equations to be considered is " +
                    str(num_solns) + ", do you want to proceed?" +
                    " If yes, press 'c' then 'enter'.")
        if txt != 'c':
            print("You input: " + txt + ", exiting...")
            exit(1)
        if multiproc == True:
            jobs = []
            runner = mp.Process(target=solution_saving_worker,
                             args=(queue, num_solns, hof))
            runner.start()
            for soln in enum.exhaustive_global_search(
                                                 maximum_tree_complexity_index):
                jobs.append(soln)
                iter = iter + 1
                print('\r' + "Progress: " + str(iter/num_solns), end='')
            results = parmap.map(main_queue, jobs, queue=queue,
                                 pm_pbar=True, pm_chunksize=3)
            runner.join()
        elif multiproc == False:
            for soln in enum.exhaustive_global_search(
                                                 maximum_tree_complexity_index):
                result = main(soln, SR_config)
                score = result.fitness
                hof.update([result])
                iter = iter + 1
                if score < best_score:
                    best_score = score
                if iter % frequency_printing == 0:
                    print("best score:" + str(best_score),
                          'current score:' + str(score),
                          'at iteration:'+ str(iter), end='\x1b[1K\r')
        else:
            raise Exception("Invalid value multiproc must be true/false")
    elif exhaustive == False:
        num_solns = n_iters
        seeds = create_seeds(start_time, n_iters)
        if multiproc == True:
            runner = mp.Process(target=solution_saving_worker,
                             args=(queue, num_solns, hof))
            runner.start()
            results = parmap.map(main_rando_queue, seeds, enum=enum,
                                 max_tree_complx=maximum_tree_complexity_index,
                                 queue=queue, pm_pbar=True, pm_chunksize=3)
            runner.join()
        elif multiproc == False:
            for soln in enum.uniform_random_global_search(
                                                  maximum_tree_complexity_index,
                                                                n_iters, seeds):
                result = main(soln, SR_config)
                score = result.fitness
                hof.update([result])
                iter = iter + 1
                if score < best_score:
                    best_score = score
                if iter % frequency_printing == 0:
                    print("best score:" + str(best_score),
                          'current score:' + str(score),
                          'at iteration:'+ str(iter), end='\x1b[1K\r')
        else:
            raise Exception("Invalid multiproc, must be true/false")
    else:
        raise Exception("Invalid value for exhaustive")
    totalTime = time.time() - start_time
    print("\nTotal time: ", totalTime)    
        
    #    # save halloffame, sr_config, at output_db, with key == timestamp
    #    with SqliteDict(output_db, autocommit=False) as results_dict:
    #        nowtime = str(datetime.datetime.now())
    #        results_dict[nowtime] = [hof, SR_config]