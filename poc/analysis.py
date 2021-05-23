# %%
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %%
NLAT = 65
NLON = 73
lats = np.arange(30, 46.25, 0.25)
lons = np.arange(128, 146.25, 0.25)
assert len(lats) == NLAT
assert len(lons) == NLON

domains = {
    "Hokkaido": [41.5, 140, 45.5, 145.0],
    "Tohoku": [37.0, 139.5, 41.25, 141.75],
    "Chuo": [34.75, 137.75, 36.0, 140.75],
    "Kanto": [36.0, 138.75, 37.0, 140.75],
    "Chubu": [34.5, 136.75, 36.25, 138.50],
    "Hokuriku": [36.25, 136.75, 37.0, 137.75],
    "Kinki": [34.75, 134.25, 35.5, 136.75],
    "Shikoku": [32.75, 132.5, 34.5, 134.5],
    "Chugoku": [34.0, 131.0, 35.5, 134.5],
    "Kyusyu": [31.25, 130.0, 34.0, 131.5],
}

cdomains = dict()
for domain in domains.items():
    locs = domain[1]
    clipped_loc = [
        ((lats - locs[0]) ** 2).argmin(),
        ((lons - locs[1]) ** 2).argmin(),
        ((lats - locs[2]) ** 2).argmin(),
        ((lons - locs[3]) ** 2).argmin(),
    ]
    cdomains[domain[0]] = clipped_loc


def read_data(dpath):
    return np.fromfile(dpath, np.float32).reshape(-1, NLAT, NLON)


def make_pmask(cdomains):
    pmask = np.zeros([65, 73])
    for idx, dom in enumerate(cdomains.items()):
        pmask[dom[1][0] : dom[1][2], dom[1][1] : dom[1][3]] = idx + 1
    return pmask


def aggregate_by_mask(data, pmask, domains):
    dsum = data.sum(axis=0)
    record = []
    for idx in range(len(domains)):
        mask = np.zeros([NLAT, NLON])
        mask[pmask == idx] = 1
        value = (dsum * mask).mean()
        record.append(value)
    return record


def main(dpath, year, outpath="./record.csv", overwrite=False):
    pmask = make_pmask(cdomains)
    data = read_data(dpath)
    record = aggregate_by_mask(data, pmask, domains)
    region_names = [domain[0] for domain in domains.items()]
    years = [year for i in range(len(domains))]
    df = pd.DataFrame([region_names, years, record]).T
    df.columns = ["region", "year", "record"]
    print(df)
    if not os.path.exists(outpath) or overwrite:
        df.to_csv(outpath, header=True, index=None)
    else:
        df.to_csv(outpath, mode="a", header=None, index=None)


main("./2015_oct.bin", 2015, overwrite=True)
main("./2016_oct.bin", 2016)
main("./2017_oct.bin", 2017)
main("./2018_oct.bin", 2018)
main("./2019_oct.bin", 2019)

df = pd.read_csv("./record.csv")
df.year = df.year.astype(np.int32)
sns.lineplot(x="year", y="record", hue="region", data=df)
plt.xticks(range(2015, 2020), rotation=45)
plt.xlim(2015, 2021)
sns.despine()
plt.title("ECMWF 46-day forecasts", weight="bold", loc="left")
plt.savefig("timeseries_forecast.png", dpi=300, bbox_inches="tight", pad_inches=0)
