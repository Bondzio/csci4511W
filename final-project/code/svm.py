# CSCI 4511W Final Project
# University of Minnesota
# Code by Brian Cooper
# This file sets up the quantum and classical support vector machines.
from datasets import *
import numpy as np
from qiskit.aqua.utils import split_dataset_to_data_and_labels
from qiskit.aqua.input import ClassificationInput
from qiskit.aqua import run_algorithm
# from qiskit_qcgpu_provider import QCGPUProvider

# ============================================================================ #
# Quantum support vector machine                                               #
#   train_input:  training set                                                 #
#   test_input:   testing set                                                  #
#   n:            projected input dimensionality                               #
# ============================================================================ #
def quantum_svm(train_input, test_input, class_labels, n):
    temp = [test_input[k] for k in test_input]
    total_array = np.concatenate(temp)

    # Select parameters based on number of classes in data
    if len(class_labels) > 2:
        aqua_dict = {
            'problem': {'name': 'classification', 'random_seed': 100},
            'algorithm': {
                'name': 'QSVM'
            },
            'feature_map': {'name': 'SecondOrderExpansion', 'depth': 2, \
                'entangler_map': [[0, 1]]},
            'multiclass_extension': {'name': 'AllPairs'},
            'backend': {'name': 'qasm_simulator', 'shots': 256}
        }
    else:
        aqua_dict = {
            'problem': {'name': 'classification', 'random_seed': 100},
            'algorithm': {
                'name': 'QSVM'
            },
            'feature_map': {'name': 'SecondOrderExpansion', 'depth': 2, \
                'entangler_map': [[0, 1]]},
            'backend': {'name': 'qasm_simulator', 'shots': 256}
        }

    # Use the QCGPUProvider for improved performance
    # If using, make sure to enable the import code on line 6
    # backend = QCGPUProvider().get_backend('qasm_simulator')

    algo_input = ClassificationInput
    algo_input.training_dataset = train_input
    algo_input.test_dataset = test_input
    algo_input.datapoints = total_array

    # Run the quantum SVM algorithm
    # Use the second version if using the QCGPUProvider backend (GPU)
    result = run_algorithm(aqua_dict, algo_input)
    # result = run_algorithm(aqua_dict, algo_input, backend=backend)

    # Print model values
    # for k,v in result.items():
    #   print("'{}' : {}".format(k, v))

    return result

# ============================================================================ #
# Classical support vector machine (Radial basis kernel)                       #
#   train_input:  training set                                                 #
#   test_input:   testing set                                                  #
#   n:            projected input dimensionality                               #
# ============================================================================ #
def classical_svm(train_input, test_input, class_labels, n):
    temp = [test_input[k] for k in test_input]
    total_array = np.concatenate(temp)

    # Select parameters based on number of classes in data
    if len(class_labels) > 2:
        aqua_dict = {
            'problem': {'name': 'classification', 'random_seed': 100},
            'algorithm': {
                'name': 'SVM'
            },
            'multiclass_extension': {'name': 'AllPairs'}
        }
    else:
        aqua_dict = {
            'problem': {'name': 'classification', 'random_seed': 100},
            'algorithm': {
                'name': 'SVM'
            }
        }

    algo_input = ClassificationInput
    algo_input.training_dataset = train_input
    algo_input.test_dataset = test_input
    algo_input.datapoints = total_array

    # Run the classical SVM algorithm
    result = run_algorithm(aqua_dict, algo_input)

    # Print model values
    #  for k,v in result.items():
    #      print("'{}' : {}".format(k, v))

    return result
