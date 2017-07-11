# iou

A python module using networkx, pyomo and ipopt to solve for the optimally minimum number of transactions to settle debts/expenses between friends.

<p align="center">
<img src="https://raw.githubusercontent.com/kdheepak89/iou/master/screenshots/screenshot1.png" width="400" >
</p>

## Install

    pip install py-iou
    pip install py-iou --upgrade

### Dependencies

* Install [`ipopt`](https://projects.coin-or.org/Ipopt)

If you have [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html), you can install it using the following command.

```bash
conda install -c conda-forge ipopt
```

## Run

* Run the following to find the optimal transactions using input from transactions.csv

        iou --data iou/data/transactions.csv

    OR

        iou --data iou/data/transactions.csv --verbose

<p align="center">
<img src="https://raw.githubusercontent.com/kdheepak89/iou/master/screenshots/screenshot2.png" align="center" width="400" >
</p>

Use help

    iou --help

A transactions.csv file is required to find the optimal order

## Contribution

Feel free to submit a pull request.


