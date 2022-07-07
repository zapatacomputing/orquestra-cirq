# orquestra-cirq

## What is it?

`orquestra-cirq` is a [Zapata](https://www.zapatacomputing.com) library holding modules for integrating cirq and qsimcirq with [Orquestra](https://www.zapatacomputing.com/orquestra/).

## Installation

Even though it's intended to be used with Orquestra, `orquestra-cirq` can be also used as a Python module.
To install it, make to install `orquestra-quantum` first. Then you just need to run `pip install .` from the main directory.
If you want to import `QSimSimulator`, you are requried to run `pip install -e .[qsim].` 
## Overview

`orquestra-cirq` is a Python module that exposes Cirq's and qsim's simulators as an [`orquestra`](https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend.py) `QuantumSimulator`. They can be imported with:

```
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.integrations.cirq.simulator.qsim_simulator import QSimSimulator
```

The parameters to configure GPU executions are supplied to `QSimSimulator` as `QSimOptions`. The details of these parameters can be found in [qsimcirq python interface](https://quantumai.google/qsim/cirq_interface#gpu_execution). Below is an example of passing `use_gpu` parameter to the `QSimSimulator`:

```
from orquestra.integrations.cirq.simulator.qsim_simulator import QSimSimulator

from qsimcirq import QSimOptions

qsim_options = QSimOptions(use_gpu=True)

sim = QSimSimulator(qsim_options=qsim_options)
```

In addition, it interfaces with the noise models and provides converters that allow switching between `cirq` circuits and those of `orquestra`.

The module can be used directly in Python or in an [Orquestra](https://www.orquestra.io) workflow.
For more details, see the [Orquestra Core docs](https://zapatacomputing.github.io/orquestra-core/index.html).

For more information regarding Orquestra and resources, please refer to the [Orquestra documentation](https://www.orquestra.io/docs).

## Development and contribution

You can find the development guidelines in the [`orquestra-quantum` repository](https://github.com/zapatacomputing/orquestra-quantum).
