# Georgios Koliopoulos (2646502)

import pandas as pd

tables = pd.read_html("https://www.ref.org.uk/generators/index.php?start=0&order=AvAnnMWh&dir=desc")
generators = tables[1]

for i in range(100, 15500, 100):
    table = pd.read_html("https://www.ref.org.uk/generators/index.php?start=%s&order=AvAnnMWh&dir=desc" % i)
    generators_sub_list = table[1]
    generators = generators.append(generators_sub_list, ignore_index=True)


generators.to_csv
