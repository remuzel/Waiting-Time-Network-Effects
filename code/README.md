## How to run the simulation

To run the simulation, first make sure you have the (short) list of dependencies:

```
> pip install -r requirements.txt
```

To see a list of all parameters and their descriptions run:

```
> python main.py --help
```

Then simply run the simulation with your desired parameters. The set that generate the results from figure 4.1 in the report are:

```
> python main.py --it 100 --P 2 --mu_r 0.25 0.05 --mu_d 0.9 0.2 --eta 0 0 --delays 0 65
```


---

## Bellow you fill find the results of my succesful experimentations.

### After training the simulation on 70% of the data:

```
> python main.py --it 100 --P 3 --mu_r 0.15 0.05 0.05 --mu_d 0.8 0.1 0.2 --eta 0 0 0 --delay 0 65 65
```

Where the RMSE scores are 0.09840443570650487, 0.04302963532198344, 0.04791568003183646 for each platform respectively

```
> python main.py --it 100 --P 2 --mu_r 0.25 0.05 --mu_d 0.9 0.2 --eta 0 0 --delay 0 65
```

Where the RMSE scores are 0.10718332729106592, 0.05646036378962575 for each platform respectively

---

### After training the simulation on 100% of the data:

```
> python main.py --it 100 --P 3 --mu_r 0.15 0.05 0.05 --mu_d 0.9 0.1 0.2 --eta 0 0 0 --delay 0 65 65
```

Where the RMSE scores are 0.08978965413090538, 0.0515823122232287, 0.040303459779692886 for each platform respectively

```
> python main.py --it 100 --P 2 --mu_r 0.25 0.05 --mu_d 0.9 0.2 --eta 0 0 --delay 0 65
```

Where the RMSE scores are 0.0904486915979686, 0.049763603189207854 for each platform respectively

---
