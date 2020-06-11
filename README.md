# Waiting-Time-Network-Effects


[Uber has 3.5m regular passengers, and 45,000 licensed drivers in London
alone.](https://www.ft.com/content/78827b06-0f6a-11ea-a225-db2f231cfeae?accessToken=zwAAAW6nzFMAkc94gnsGD2oR6tOiJdsvIxz-rg.MEUCIDrfHHtCUtkTvk0Q-TynG3BAr4HpGgtd0nYzsOBqrUyqAiEA3KC-UmPZmvEXhd7sNAIRT69TlKnExRU011ApbzLB2fo&sharetype=gift?token=c4079894-3bb0-4a18-9bd6-28c637fc418c)

---

After training the simulation on 50% of the data:

optimal is
> `python main.py --it 100 --P 3 --mu_r 0.2 0.1 0.1 --mu_d 0.8 0.2 0.6 --eta 0 0 0 --delay 0 65 65`

---

After training the simulation on the middle 50% of the data:

optimal is
> `python main.py --it 100 --P 3 --mu_r 0.4 0.1 0.1 --mu_d 0.4 0.8 0.2 --eta 0 0 0 --delay 0 65 65`

--- 

After training the simulation on 70% of the POPULATION data:

optimal is
> `python main.py --it 100 --P 3 --mu_r 0.1 0.8 0.3 --mu_d 0.2 0.2 0.8 --eta 0 0 0 --delay 0 65 65`

---

After training the simulation on 70% of the data:

optimal is
> `python main.py --it 100 --P 3 --mu_r 0.15 0.05 0.05 --mu_d 0.8 0.1 0.2 --eta 0 0 0 --delay 0 65 65`
Where the RMSE scores are 0.09840443570650487, 0.04302963532198344, 0.04791568003183646 for each platform respectively

---

After training the simulation on 100% of the data:

optimal is 
> `python main.py --it 100 --P 3 --mu_r 0.15 0.05 0.05 --mu_d 0.9 0.1 0.2 --eta 0 0 0 --delay 0 65 65`
Where the RMSE scores are 0.08978965413090538, 0.0515823122232287, 0.040303459779692886 for each platform respectively

---
